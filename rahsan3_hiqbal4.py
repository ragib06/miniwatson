
# NLP Project Part 2
# Use this as the main class for your project. 
# Implement the logic to generate the SQL query and the query answer.
# Create additional methods, variables, and classes as needed.

from stat_parser import Parser
from sqlite_db_manager import SqliteManager
from semantic_analyser import SemanticAnalyser
from utils import Utils
from semantic_sql import SemanticSQLBuilder
import infer_domain


databases = {
    'Movie' :   'sqlitedb/oscar-movie_imdb.sqlite',
    'Music' :   'sqlitedb/music.sqlite',
    'Geography' :   'sqlitedb/WorldGeography.sqlite'
}

parser = Parser()
db_manager = None
infer_domain.init()

currentQuery = ""
sqlQuery = None


def printSQL(question, domain):
    try:
        tree = parser.parse(question)
        sem_analyser = SemanticAnalyser()
        semantic = sem_analyser.getSemanticFromParseTree(q, tree)

        print "<SQL>"

        if semantic is None:
            print ''
            return None
        else:
            sql_builder = SemanticSQLBuilder(semantic, domain)
            sql_queries = sql_builder.build_sql_from_semantic()

        print '\n'.join(sql_queries)
        return sql_queries
    except:
        return None


def printAnswer(sql_query):

    answer = "I don't know"

    if (sql_query is not None) and len(sql_query) > 0:
        result = db_manager.processQueries(sql_query)
        if result is not None:
            answer = result

    print("<ANSWER>\n" + str(answer) )

print("Welcome! This is MiniWatson. \n")
print("Please ask a question. Type 'q' when finished. \n")
print("\n")

inputString = raw_input("").strip(" ")
while inputString != "q":
    currentQuery = inputString
    print("<QUERY>\n" + currentQuery)

    domain = infer_domain.Domain.MOVIE

    try:
        domain = infer_domain.infer_domain(currentQuery)
        domain = domain[0][0]

        db_manager = SqliteManager(databases[infer_domain.domain_descriptor(domain)])

        q = Utils.preprocess_question(currentQuery)
        sql = printSQL(q, domain)
        printAnswer(sql)
        print '\n'
    except Exception as error:
        # print error
        print "<ANSWER>\nI don't know\n"

    inputString = raw_input("").strip(" ")
print("Goodbye. \n")
