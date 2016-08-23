from nltk import word_tokenize
from collections import defaultdict
from nltk.corpus import stopwords
from stat_parser import Parser
from nltk import *
import nltk
from nltk.corpus import wordnet as wn
import sys, getopt, codecs


movie_keys = ['movie', 'oscar', 'actor', 'direct', 'director', 'star']
music_keys = ['sing', 'album', 'music', 'track']
geography_keys = ['country', 'capital', 'continent', 'mountain', 'deep', 'high']

domain_keys = [movie_keys, music_keys, geography_keys]
domain_syn = [{}, {}, {}]

parser = None


def enum(**enums):
    return type('Enum', (), enums)

Domain = enum(MOVIE=0, MUSIC=1, GEOGRAPHY=2)

def domain_descriptor(domain_index):
    if domain_index == Domain.MOVIE:
        return "Movie"
    elif domain_index == Domain.GEOGRAPHY:
        return "Geography"
    elif domain_index == Domain.MUSIC:
        return "Music"



def load_questions(filename):
    questions = []

    with codecs.open(filename, 'r', 'utf-8') as f:
        for line in f:
            questions.append(line.strip())
    return questions

def remove_stopwords(sentence):
     stopwords = nltk.corpus.stopwords.words('english')
     content = [w for w in sentence if w.lower() not in stopwords]
     return content

# def find_path_similarity(dom_wrd_lst, tok_sentence):
#     score = 0.0
#     for sent_word in tok_sentence:
#         if wn.synsets(sent_word):
#             sent_syn = wn.synsets(sent_word)[0]
#             for wrd in dom_wrd_lst:
#                 dom_syn = wn.synsets(wrd)[0]
#                 if sent_syn.path_similarity(dom_syn) is not None:
#                     score = score + sent_syn.path_similarity(dom_syn)

#     return score

def find_path_similarity(domain, words):
    score = 0.0
    for word in words:
        word_syns = wn.synsets(word)
        if (word_syns is not None) and (len(word_syns) > 0):
            word_syn = word_syns[0]
            for key in domain_keys[domain]:
                dom_syn = domain_syn[domain][key]
                if word_syn.path_similarity(dom_syn) is not None:
                    score = score + word_syn.path_similarity(dom_syn)

    return score


def infer_domain(question):

    global Domain

    words = remove_stopwords(word_tokenize(question[:-1]))    

    max_similarity = 0.0
    domain = -1

    domain_similarities = {}
    total_similarity_weight = 0.0

    similarity = find_path_similarity(Domain.MOVIE, words)
    total_similarity_weight += similarity
    domain_similarities[Domain.MOVIE] = similarity

    if similarity > max_similarity:
        max_similarity = similarity
        domain = Domain.MOVIE

    similarity = find_path_similarity(Domain.MUSIC, words)
    total_similarity_weight += similarity
    domain_similarities[Domain.MUSIC] = similarity
    
    if similarity > max_similarity:
        max_similarity = similarity
        domain = Domain.MUSIC

    similarity = find_path_similarity(Domain.GEOGRAPHY, words)
    total_similarity_weight += similarity
    domain_similarities[Domain.GEOGRAPHY] = similarity

    if similarity > max_similarity:
        max_similarity = similarity
        domain = Domain.GEOGRAPHY

    domain_similarities[Domain.MOVIE] = domain_similarities[Domain.MOVIE] / total_similarity_weight
    domain_similarities[Domain.MUSIC] = domain_similarities[Domain.MUSIC] / total_similarity_weight
    domain_similarities[Domain.GEOGRAPHY] = domain_similarities[Domain.GEOGRAPHY] / total_similarity_weight

    domain_similarities = [(i, domain_similarities[i]) for i in range(len(domain_similarities))]
    domain_similarities = sorted(domain_similarities, key=lambda x: -x[1])
    
    return domain_similarities

    # return (domain, max_similarity/total_similarity_weight)



def print_output(question_dict):
    with open('output.txt', 'w') as out:
        out_string = ''
        for q in question_dict.keys():
            dom = question_dict[q]
            out_string += '<QUESTION> ' + str(q.encode('utf8')) + '\n'

            # dom = infer_domain(q)
            out_string += '<CATEGORY> ';
            out_string += domain_descriptor(dom[0][0]) + '(' + str(round(dom[0][1] * 100, 2)) + '%), '
            out_string += domain_descriptor(dom[1][0]) + '(' + str(round(dom[1][1] * 100, 2)) + '%), '
            out_string += domain_descriptor(dom[2][0]) + '(' + str(round(dom[2][1] * 100, 2)) + '%)\n'

            parse_tr = parser.parse(q)
            out_string += '<PARSETREE> ' + '\n'
            out_string += str(parse_tr)
            out_string += '\n\n'
        print out_string
        out.write(out_string)


def init():
    global parser, movie_keys, music_keys, geography_keys, domain_syn, Domain

    parser = Parser()
    
    for key in movie_keys:
        domain_syn[Domain.MOVIE][key] = wn.synsets(key)[0]

    for key in music_keys:
        domain_syn[Domain.MUSIC][key] = wn.synsets(key)[0]

    for key in geography_keys:
        domain_syn[Domain.GEOGRAPHY][key] = wn.synsets(key)[0]


def process_file(filename):
    questions = load_questions(filename)
    
    q_dict = {}
    for q in questions:
        q_dict[q] = infer_domain(q)

    print_output(q_dict)

def main():
    init()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:q:h")
    except getopt.GetoptError as err:
        print str(err)
        sys.exit(2)

    if len(sys.argv) == 2:
        process_file(sys.argv[1])
        sys.exit(0)

    if len(opts) < 1:
        print len(opts)
        print "ERROR: Not enough arguments"
        print "try help: python infer_domain.py -h"
        sys.exit(2)

    for o, a in opts:
        if o == "-f":
            process_file(a)
        elif o == "-q":
            dom = infer_domain(a)
            out_string = a + " => ["
            out_string += domain_descriptor(dom[0][0]) + '(' + str(round(dom[0][1] * 100, 2)) + '%), '
            out_string += domain_descriptor(dom[1][0]) + '(' + str(round(dom[1][1] * 100, 2)) + '%), '
            out_string += domain_descriptor(dom[2][0]) + '(' + str(round(dom[2][1] * 100, 2)) + '%)]'
            print out_string
            # print a, "=>", "(" + domain_descriptor(dom[0]) + ", " + str(round(dom[1] * 100, 2)) + "%)"

        elif o == "-h":
            print "python infer_domain.py -f [filename of the file containing questions]"
            print "python infer_domain.py -q [a single question string]"

        else:
            print "try help: python infer_domain.py -h"
            pass





if __name__ == "__main__":
    main()





#TODO fails in the following sentences
#Was Beyonce born in the USA?






#ignore the rest, may or may not be useful later

#
# parser = Parser()
# tr = parser.parse('is rome capital of italy')

# for s in syns:
#     for l in s.lemmas():
#         print l
#     print s.path_similarity()
#     print s.topic_domains()
#     print s.usage_domains()
#     print s.attributes()
#     print s.causes()
#     print s.definition()
#     print s.examples()
#     print '_______________________________________'



# domain2synsets = defaultdict(list)
# synset2domains = defaultdict(list)
# for i in open('wn-domains-3.2-20070223', 'r'):
#     ssid, doms = i.strip().split('\t')
#     doms = doms.split()
#     synset2domains[ssid] = doms
#     for d in doms:
#         domain2synsets[d].append(ssid)
#
# print '---------'
#
# for it in wn.synsets('music'):
#     print it.offset()
# #print k
# print synset2domains.get('00001740-n')
#
# for i in range(4):
#   item = synset2domains.popitem()
#   print item

