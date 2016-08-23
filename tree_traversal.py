import nltk
from nltk.sem.logic import Expression
from semgram_generator import generate_semgram

grammer = nltk.data.load("grammars/simplest.cfg")
rexp = Expression.fromstring

parser = nltk.ChartParser(grammer)
tr = parser.parse("i read books".split())

generate_semgram(tr)