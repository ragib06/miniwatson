__author__ = 'ragib'

from utils import Utils

def build_sql_for__does(pparam):

    WH = pparam['wh']
    NP = pparam['np']
    IsAlbum = pparam['isalbum']

    lst_sql = []

    if WH:
        if IsAlbum:
            lst_sql.append("select a.name "
                       "from Album a "
                       "inner join Track t on a.albumId == t.albumId "
                       "where t.name like '%" + "%' and t.name like '%".join(NP[0:]) + "%'")

    else:
        if IsAlbum and len(NP) >= 2:
            lst_sql.append("select count(*) "
                       "from Track t "
                       "inner join Album a on a.albumId == t.albumId "
                       "where a.name like '%" + NP[0] + "%' and t.name like '%" + "%' and t.name like '%".join(NP[1:]) + "%'")

            lst_sql.append("select count(*) "
                       "from Track t "
                       "inner join Album a on a.albumId == t.albumId "
                       "where a.name like '%" + NP[-1] + "%' and t.name like '%" + "%' and t.name like '%".join(NP[:-1]) + "%'")

    return lst_sql



def build_sql_for__did(pparam):

    WH = pparam['wh']
    NP = pparam['np']

    lst_sql = []

    if len(NP) >= 2:
        lst_sql.append("select count(*) "
                       "from Track t "
                       "inner join Album a on a.albumID == t.albumID "
                       "inner join Artist ar on ar.id == a.artsitID "
                       "where ar.name like '%" + NP[0] + "%' and "
                       "t.name like '%" + "%' and t.name like '%".join(NP[1:]) + "%'")

        lst_sql.append("select count(*) "
                       "from Track t "
                       "inner join Album a on a.albumID == t.albumID "
                       "inner join Artist ar on ar.id == a.artsitID "
                       "where ar.name like '%" + NP[-1] + "%' and "
                       "t.name like '%" + "%' and t.name like '%".join(NP[:-1]) + "%'")

    return lst_sql


def build_sql_for__sings(pparam):

    WH = pparam['wh']
    NP = pparam['np']

    lst_sql = []

    if WH:
        if len(NP) >= 1:
            lst_sql.append("select ar.name "
                       "from Artist ar "
                       "inner join Album a on ar.id == a.artsitID "
                       "inner join Track t on a.albumID == t.albumID "
                       "where t.name like '%" + "%' and t.name like '%".join(NP) + "%'")


    else:
        pass

    return lst_sql



def build_sql_for__released(pparam):

    WH = pparam['wh']
    NP = pparam['np']
    Year = pparam['year']

    lst_sql = []

    if WH:
        if (Year is not None) and len(NP) == 1:
            lst_sql.append("select a.name "
                       "from Album a "
                       "inner join Artist ar on ar.id == a.artsitID "
                       "where ar.name like '%" + NP[0] + "%' "
                       "and a.releaseDate >= '" + Year + "-1-1' and a.releaseDate < '" + str(int(Year)+1) + "-1-1'")


    else:
        pass

    return lst_sql