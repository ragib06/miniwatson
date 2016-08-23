__author__ = 'ragib'

from utils import Utils


def build_sql_for__is(pparam):

    WH = pparam['wh']
    NP = pparam['np']
    Cast = pparam['cast']
    Year = pparam['year']
    Movie = pparam['movie']

    lst_sql = []

    if WH:
        if (Cast is not None) and (Movie is not None) and len(NP) > 0:
            NP = NP[0]
            lst_sql.append("select p.name"
                   " from person p"
                   " inner join director d on p.id = d.director_id"
                   " inner join movie m on d.movie_id = m.id"
                   " and m.name like '%" + NP + "%'")

    else:
        if Cast == 'director':  #Is Kubrick a director?
            lst_sql.append("select count(*) "
                           " from person p "
                           " inner join director d on p.id = d.director_id "
                           " where p.name like '%" + NP[0] + "%'")

        elif (Cast == 'actor') or (Cast == 'actress'):   #Is Neeson an actor?
            lst_sql.append("select count(*) "
                           " from person p "
                           " inner join actor a on p.id = a.actor_id "
                           " where p.name like '%" + NP[0] + "%'")

        elif len(NP) in [2, 3]:   #Is MightyAphrodite by Allen?
            lst_sql.append("select count(*)"
                           " from person p "
                           " inner join director d on p.id = d.director_id"
                           " inner join movie m on m.id = d.movie_id"
                           " where p.name like '%" + NP[0] + "%' and m.name like '%" + NP[-1] + "%'")

            lst_sql.append("select count(*)"
                           " from person p "
                           " inner join director d on p.id = d.director_id"
                           " inner join movie m on m.id = d.movie_id"
                           " where p.name like '%" + NP[-1] + "%' and m.name like '%" + NP[0] + "%'")

        elif (Movie is not None) and len(NP)>0 and (Year is not None):
            NP = NP[0]
            lst_sql.append("select count(*)"
                           " from movie m"
                           " inner join oscar o on m.id = o.movie_id"
                           " where m.name like '%" + NP + "%'and o.year = '" + Year + "' and o.type = 'BEST-PICTURE'")

    return lst_sql


def build_sql_for__win(pparam):

    WH = pparam['wh']
    NP = pparam['np']
    Nationality = pparam['nationality']
    Cast = pparam['cast']
    Year = pparam['year']
    Movie = pparam['movie']

    lst_sql = []

    # consider the first NP only
    # todo: check for improvement and test cases
    if (NP is not None) and (len(NP) > 0):
        NP = NP[0]

    if WH:  # WH- questions
        if (Nationality is not None) and (Cast is not None) and (Year is not None):
            lst_sql.append("select p.name"
                           " from person p"
                           " inner join actor a on p.id = a.actor_id"
                           " inner join oscar o on a.movie_id = o.movie_id"
                           " where p.pob like '%" + Utils.find_country(Nationality) + "%'"
                           " and o.year = '" + Year + "'"
                           " and o.type like '%" + Cast + "%'"
                           )

        elif (NP is not None) and (Cast is not None):
            lst_sql.append("select o.year from oscar o"
                           " inner join person p on o.person_id = p.id"
                           " where p.name like '%" + NP + "%'"
                           " and o.type like '%best-" + Cast +"%'")

        elif (Movie is not None) and (NP is not None):
            lst_sql.append("select m.name"
                           " from movie m"
                           " inner join oscar o on m.id = o.movie_id"
                           " inner join actor a on m.id = a.movie_id"
                           " inner join person p on p.id = a.actor_id"
                           " where p.name like '%" + NP + "%'")

        elif (Cast is not None) and (Year is not None):
            lst_sql.append("select p.name"
                       " from person p"
                       " inner join oscar o on p.id = o.person_id"
                       " where o.year = '" + Year +"'"
                       " and o.type like '%" + "best-"+ Cast + "%'")

        elif (Movie is not None) and (Year is not None):
            lst_sql.append("select m.name from movie m"
                           " inner join oscar o on m.id = o.movie_id"
                           " where o.type like '%best-picture%' "
                           " and o.year = '" + Year + "'")

    else:
        if (Year is not None) and (Nationality is not None) and (Cast is not None):
            lst_sql.append("select count(*)"
                           " from person p"
                           " inner join actor a on p.id = a.actor_id"
                           " inner join oscar o on a.movie_id = o.movie_id"
                           " where p.pob like '%" + Utils.find_country(Nationality) + "%'"
                           " and o.year = '" + Year + "'"
                           " and o.type like '%" + Cast + "%'"
                           )
        elif (Cast is not None) and (Year is not None) and (NP is not None):
            lst_sql.append("select count(*)"
                       " from person p"
                       " inner join oscar o on p.id = o.person_id"
                       " where o.year = '" + Year +"'"
                       " and o.type like '%" + "best-" + Cast + "%'")

        elif (Year is not None) and (NP is not None):
            lst_sql.append("select count(*)"  # if it's a movie
                   " from movie m"
                   " inner join oscar o on m.id = o.movie_id"
                   " where m.name like '%" + NP + "%'  and o.year = '" + Year + "'")

            lst_sql.append("select count(*)"  # if it's a person # win(2000,Swank)
                   " from person p"
                   " inner join oscar o on p.id = o.person_id"
                   " where p.name like '%" + NP + "%' and o.year = '" + Year + "'")

        elif (Movie is not None) and (NP is not None):
            lst_sql.append("select count(*)"
                   " from person p"
                   " inner join actor a on p.id = a.actor_id"
                   " inner join oscar o on a.movie_id = o.movie_id"
                   " where p.name like '%" + NP + "%'")

    return lst_sql


def build_sql_for__born(pparam):

    WH = pparam['wh']
    NP = pparam['np']
    Location = pparam['location']

    NP = NP[0] if Location != NP[0] else NP[1]

    lst_sql = []

    if WH:
        lst_sql.append("select pob"
                       " from person p"
                       " where p.name like '%" + NP + "%'")
    else:
        lst_sql.append("select count(*)"
                       " from person p"
                       " where p.name like '%" + NP + "%' and pob like '%" + Location + "%'")

    return lst_sql


def build_sql_for__did(pparam):

    NP = pparam['np']

    lst_sql = []

    lst_sql.append("select count(*) "
                       " from person p"
                       " inner join actor a on p.id = a.actor_id"
                       " inner join movie m on a.movie_id = m.id"
                       " where p.name like '%" + NP[0] + "%' and m.name like '%" + "%' and m.name like '%".join(NP[1:]) + "%'")

    lst_sql.append("select count(*) "
                       " from person p"
                       " inner join director d on p.id = d.director_id"
                       " inner join movie m on d.movie_id = m.id"
                       " where p.name like '%" + NP[0] + "%' and m.name like '%" + "%' and m.name like '%".join(NP[1:]) + "%'")

    return lst_sql


def build_sql_for__directed(pparam):
    NP = pparam['np']
    Movie = pparam['movie']
    Year = pparam['year']

    lst_sql = []

    if (Movie is not None) and (Year is not None):  #Who directed SchindlersList?, param1: 'y' param2: movieName
        lst_sql.append("select p.name from person p"
                       " inner join director d on p.id = d.director_id"
                       " inner join oscar o on o.movie_id = d.movie_id"
                       " where o.type like 'best-picture' and o.year = '" + Year + "'")

    elif len(NP) >= 1:
        lst_sql.append("select p.name"
                   " from person p"
                   " inner join director d on p.id = d.director_id"
                   " inner join movie m on d.movie_id = m.id"
                   " and m.name like '%" + NP[0] + "%'")


    return lst_sql
