"""
This class creates database connection and executes sqls
"""
import sqlite3


class SqliteManager:

    def __init__(self, dbname):
        conn = sqlite3.connect(dbname)
        self.c = conn.cursor()

    def execQuery(self, sql):
        return self.c.execute(sql)

    def processQueries(self, queries):

        result_parser = SqliteResultParser()

        if len(queries) > 1:
            sum = 0
            for q in queries:
                for row in self.execQuery(q):
                    for it in row:
                        sum += it
            return "yes" if sum > 0 else "no"
        else:
            result = self.execQuery(queries[0])
            return result_parser.parseDbResult(result)


class SqliteResultParser:

    def __init__(self):
        pass

    @staticmethod
    def parseDbResult(result):
        for row in result:
            for item in row:
                if (isinstance(item, int)):
                    if (item <= 20):
                        return "yes" if item > 0 else "no"
                    else:
                        return item
                else:
                    return ''.join(item)



