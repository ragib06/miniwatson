__author__ = 'ragib'

from utils import Utils


def build_sql_for__is(pparam):

    WH = pparam['wh']
    NP = pparam['np']
    Capital = pparam['capital']
    Continent = pparam['continent']
    Location = pparam['location']
    Sea = pparam['sea']
    Comparison = pparam['comparison']
    IsMountain = pparam['ismountain']
    IsOcean = pparam['isocean']

    lst_sql = []

    # print pparam

    if WH:
        if (IsMountain is not None) and (Comparison == 'height'):
            lst_sql.append("select m.Name from Mountains m order by m.Height Desc Limit 1")
        elif (IsOcean is not None) and (Comparison == 'depth'):
            lst_sql.append("select s.Ocean from Seas s order by s.Deepest Desc Limit 1")

    else:
        if Capital and len(NP) == 2:
            lst_sql.append("select count(*) "
                       "from Capitals cap "
                       "inner join Cities ct on ct.id = cap.CityId "
                       "inner join Countries cn on cn.id = cap.CountryId "
                       "where cn.Name like '%" + NP[0] + "%' and ct.Name like '%" + NP[1] + "%'")

            lst_sql.append("select count(*) "
                       "from Capitals cap "
                       "inner join Cities ct on ct.id = cap.CityId "
                       "inner join Countries cn on cn.id = cap.CountryId "
                       "where cn.Name like '%" + NP[1] + "%' and ct.Name like '%" + NP[0] + "%'")

        elif Continent and Location:
            lst_sql.append("select count(*) "
                       "from CountryContinents cc "
                       "inner join Continents ct on ct.id = cc.ContinentId "
                       "inner join Countries cn on cn.id = cc.CountryId "
                       "where cn.Name like '%" + Location + "%' and ct.Continent like '%" + Continent + "%'")

        elif Comparison and len(Sea) == 2:
            lst_sql.append("select count(*) "
                       "from Seas s1 join Seas s2 "
                       "where s1.Ocean like '%" + Sea[0] + "%' and s2.Ocean like '%" + Sea[1] + "%' and s1.Deepest > s2.Deepest")


    return lst_sql



def build_sql_for__does(pparam):

    WH = pparam['wh']
    NP = pparam['np']
    Capital = pparam['capital']
    Continent = pparam['continent']
    IsContinent = pparam['iscontinent']
    IsBorder = pparam['isborder']
    Location = pparam['location']
    Sea = pparam['sea']
    Comparison = pparam['comparison']

    lst_sql = []

    if WH:
        if IsContinent and (Location is not None):
            lst_sql.append("select ct.Continent "
                       "from Continents ct "
                       "inner join CountryContinents cc on ct.id = cc.ContinentId "
                       "inner join Countries cn on cn.id = cc.CountryId "
                       "where cn.Name like '%" + Location + "%'")

        elif IsBorder and (len(NP) == 1) and (Location is not None):
            lst_sql.append("select cn1.Name "
                           "from Countries cn1 "
                           "inner join Borders b on b.Country2 = cn1.Id "
                           "inner join Countries cn2 on b.Country1 = cn2.Id "
                           "where cn2.Name like '%" + Location + "%' "
                           "UNION "
                           "select cn1.Name "
                           "from Countries cn1 "
                           "inner join Borders b on b.Country1 = cn1.Id "
                           "inner join Countries cn2 on b.Country2 = cn2.Id "
                           "where cn2.Name like '%" + Location + "%'")

    else:
        pass

    return lst_sql