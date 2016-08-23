from stat_parser import Parser
from sqlite_db_manager import SqliteManager
from semantic_analyser import SemanticAnalyser
from utils import Utils
from semantic_sql import SemanticSQLBuilder
import infer_domain
import logging, sys, getopt



questions = [
    'Is Kubrick a director?',
    'Is Neeson an actor?',
    'Is Mighty Aphrodite by Allen?',
    'Was Loren born in Italy?',
    'Was Birdman the best movie in 2015?',
    'Did Neeson star in Schindler\'s List?',
    'Did Swank win the oscar in 2000?',
    'Did a French actor win the oscar in 2012?',
    'Did a movie with Neeson win the oscar for best film?',
    'Who directed SchindlersList?',
    'Who won the oscar for best actor in 2005?',
    'Who directed the best movie in 2010?',
    'Which actress won the oscar in 2012?',
    'Which movie won the oscar in 2000?',
    'When did Blanchett win an oscar for best actress?',
    'Did Jamie Foxx win the oscar for best actor in 2005?',
    'Which French actor win the oscar in 2012?',
    'Which movie with Neeson win the oscar for best film?',
    'Did MerylStreep won the oscar in 2012?',
    'When did Meryl Streep won the oscar for best actress?',
    'Where did Loren born?',
    'Did Spielberg direct Schindler\'s List?'
]

questions = [
            # 'Did Madonna sing Papa Do Not Preach?',
            # 'Does the album Thriller include the track Beat It?',
            # 'Does the track Beat It appears in the album Thriller?'
            # 'In which album does Aura appear?',
            'Which album by Beyonce was released in 2014?'
            ]


databases = {
    'Movie' :   'sqlitedb/oscar-movie_imdb.sqlite',
    'Music' :   'sqlitedb/music.sqlite',
    'Geography' :   'sqlitedb/WorldGeography.sqlite'
}

parser = Parser()
db_manager = None
infer_domain.init()

def answer(q):

    domain = infer_domain.Domain.MOVIE
    try:
        domain = infer_domain.infer_domain(q)
        domain = domain[0][0]
        logging.info('Domain: %s', infer_domain.domain_descriptor(domain))

    except Exception as error:
        logging.error('Domain: %s', error)

    db_manager = SqliteManager(databases[infer_domain.domain_descriptor(domain)])

    q = Utils.preprocess_question(q)
    tree = parser.parse(q)
    logging.debug('Parse Tree: %s', str(tree))

    sem_analyser = SemanticAnalyser()
    semantic = sem_analyser.getSemanticFromParseTree(q, tree)
    logging.info('Semantic: %s', semantic)

    if semantic is  None:
        return 'I don\'t know'
    else:

        try:
            sql_builder = SemanticSQLBuilder(semantic, domain)
            sql_queries = sql_builder.build_sql_from_semantic()
            logging.info('SQL: \n%s', '\n'.join(sql_queries))

            if len(sql_queries) == 0:
                return 'I don\'t know'
            else:
                answer = db_manager.processQueries(sql_queries)
                return  answer
        except Exception as error:
            logging.error('SQL: %s', error)
            return 'I don\'t know'


def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ide")
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)

    loglevel = logging.INFO

    for o, a in opts:
        if o == "-i":
            loglevel = logging.INFO
        elif o == "-d":
            loglevel = logging.DEBUG
        elif o == "-e":
            loglevel = logging.ERROR
        else:
            loglevel = logging.INFO

    logging.basicConfig(stream=sys.stderr, format='%(levelname)s:%(message)s', level=loglevel)

    for q in questions:
        print 'Question:', q
        a = answer(q)
        print 'Answer  :', a
        print ''


if __name__ == "__main__":
    main()



























# os.environ['STANFORD_PARSER'] = '/home/anik/UIC/Semester2/421/project/stanford-parser-full-2013-11-12'
# os.environ['STANFORD_MODELS'] = '/home/anik/UIC/Semester2/421/project/stanford-parser-full-2013-11-12'
# parser = stanford.StanfordParser(model_path="/home/anik/UIC/Semester2/421/project/stanford-parser-full-2013-11-12/stanford-parser-3.3.0-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")

#
#
# #q = 'Is Kubrick a director?' #
# #q = 'Is Mighty Aphrodite by Allen?' #has (PP (IN by) (NP (NNP Allen) (. ?))))
# q = 'Was Loren born in Italy?' #has VBN born and (PP (IN in) (NP (NNP Italy))))
# #q = 'Was Birdman the best movie in 2015?' #has (PP (IN in) (NP (CD 2015))))
#
# born = lambda name, place: "from person p where name like %" +  name + "% and pob like %" + place + "%"
# direct = lambda director, movie:    ("from person p "
#                                     "inner join director d "
#                                     "inner join movie m "
#                                     "where p.id = d.director_id and p.name like '%" + director +
#                                     "%' and m.name like '%" + movie + "%'")


# tr = parser.parse(q)
