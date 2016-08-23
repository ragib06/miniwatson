__author__ = 'ragib'

from utils import Utils
from infer_domain import Domain
import logging



class SemanticSQLBuilder:

    SupportedNationalities = ['French', 'German', 'British', 'American', 'Italian']

    def __init__(self, func, domain=Domain.MOVIE):
        self.fname = self.get_func_name(func)
        self.lst_params = self.get_params(func)

        self.pparam = SemanticSQLBuilder.parse_params(self.lst_params)
        logging.debug('Semantic Param: %s', str(self.pparam))

        if domain == Domain.MOVIE:
            import semantic_sql_movie as helper

            self.func_map = {
                'is'    :   helper.build_sql_for__is,
                'was'   :   helper.build_sql_for__is,
                'did'   :   helper.build_sql_for__did,
                'win'   :   helper.build_sql_for__win,
                'won'   :   helper.build_sql_for__win,
                'born'  :   helper.build_sql_for__born,
                'directed'  :   helper.build_sql_for__directed
            }

        elif domain == Domain.GEOGRAPHY:
            import semantic_sql_geography as helper

            self.func_map = {
                'is'    :   helper.build_sql_for__is,
                'does'    :   helper.build_sql_for__does,
            }

        elif domain == Domain.MUSIC:
            import semantic_sql_music as helper

            self.func_map = {
                'did'    :   helper.build_sql_for__did,
                'does'    :   helper.build_sql_for__does,
                'sings'    :   helper.build_sql_for__sings,
                'released'  :   helper.build_sql_for__released,
            }


    def build_sql_from_semantic(self):

        sql_queries = []

        try:
            sql_queries = self.func_map[self.fname](self.pparam)
        except:
            pass

        return sql_queries

    def get_func_name(self, func):  # separate function name
        str_func = str(func)
        if(str_func.__contains__("\\")):
            return str_func[3:str_func.find('(')]
        else:
            return str_func[0:str_func.find('(')]

    def get_params(self, func):  # separate parameters
        str_func = str(func)
        return list(str_func[str_func.find('(') + 1:str_func.find(')')].split(','))

    @staticmethod
    def parse_params(params):
        WH = True if ( ('wh' in params) or (('whr' in params)) ) else False
        NP = None
        Nationality = None
        Location = None
        Cast = None
        Comparison = None
        Year = None
        Movie = True if ('movie' in params) or ('film' in params) else False
        Capital = True if ('capital' in params) else False
        IsContinent = True if ('continent' in params) else False
        IsMountain = True if ('mountain' in params) else False
        IsBorder = True if ('border' in params) else False
        IsOcean = True if ('ocean' in params) else False
        IsAlbum = True if ('album' in params) else False
        Continent = None
        Sea = None

        caps = [par for par in params if par in SemanticSQLBuilder.SupportedNationalities]
        if len(caps) > 0:
            Nationality = caps[0]

        caps = [Utils.hiphenate(par) for par in params if par[0].isupper() and par != Nationality]
        if len(caps) > 0:
            NP = caps

        caps = [par for par in params if Utils.isCountry(par)]
        if len(caps) > 0:
            Location = caps[0]

        caps = [par for par in params if Utils.isContinent(par)]
        if len(caps) > 0:
            Continent = caps[0]

        caps = [par for par in params if Utils.isSea(par)]
        if len(caps) > 0:
            Sea = caps

        if ('actor' in params) or ('actress' in params) or ('director' in params):
            if 'actor' in params:
                Cast = 'actor'
            elif 'actress' in params:
                Cast = 'actress'
            else:
                Cast = 'director'

        if ('deeper' in params) or ('deepest' in params) or ('higher' in params) or ('highest' in params):
            if ('deeper' in params) or ('deepest' in params):
                Comparison = 'depth'
            elif ('higher' in params) or ('highest' in params):
                Comparison = 'height'

        nums = [par for par in params if par.isdigit()]
        for num in nums:
            if int(num) > 1000:
                Year = num
            else:
                NP.append(num)

        return {
            'wh'            :   WH,
            'np'            :   NP,
            'nationality'   :   Nationality,
            'location'      :   Location,
            'cast'          :   Cast,
            'year'          :   Year,
            'movie'         :   Movie,
            'capital'       :   Capital,
            'continent'     :   Continent,
            'iscontinent'   :   IsContinent,
            'ismountain'    :   IsMountain,
            'sea'           :   Sea,
            'comparison'    :   Comparison,
            'isborder'      :   IsBorder,
            'isocean'       :   IsOcean,
            'isalbum'       :   IsAlbum
        }