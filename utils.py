__author__ = 'ragib'

import json

class Utils:

    nationalities_file = 'nationalities.json'

    def __init__(self):
        pass

    @staticmethod
    def preprocess_question(q):
        q = q[:-1]
        q = q.split(' ')[0].lower() + ' ' + ' '.join(q.split(' ')[1:])
        sq = q.split(' ')
        sq = [w.split('\'')[0] for w in sq]
        sq = [w.split(':')[0] for w in sq]
        sq = ['*'.join(w.split('-')) for w in sq]
        return ' '.join(sq)


    @staticmethod
    def find_country(nationality):

        json_data = json.loads(open(Utils.nationalities_file).read())
        for item in json_data:
            if (item['nationality'] == nationality):
                return item['country']

    @staticmethod
    def isCountry(country):
        json_data = json.loads(open(Utils.nationalities_file).read())
        for item in json_data:
            if (item['country'] == country):
                return True

        return False

    @staticmethod
    def isContinent(place):
        return place in ['Asia', 'Africa', 'North America', 'South America', 'Antarctica', 'Europe', 'Australia']

    @staticmethod
    def isSea(place):
        return place in ['Arctic', 'Atlantic', 'Indian', 'Pacific']

    @staticmethod
    def hiphenate(str):
        return '-'.join(str.split('*'))