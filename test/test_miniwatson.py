__author__ = 'ragib'

import unittest
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import ques_ans as watson

class TestMiniWatson(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_samples(self):

        qa = {
            'Is Kubrick a director?'    :   'yes',
            # 'Is Mighty Aphrodite by Allen?'  :   'yes',   #wrong domain
            'Was Loren born in Italy?'  :   'yes',
            'Was Birdman the best movie in 2015?'   :   'yes',
            'Did Neeson star in Schindler\'s List?'    :   'yes',
            'Did Swank win the oscar in 2000?'  :   'yes',
            'Did a French actor win the oscar in 2012?' :   'yes',
            'Did a movie with Neeson win the oscar for best film?'  :   'yes',
            'Who directed Schindler\'s List?'  :   'Steven Spielberg',
            'Who won the oscar for best actor in 2005?' :   'Jamie Foxx',
            'Who directed the best movie in 2010?'  :   'Kathryn Bigelow',
            'Which actress won the oscar in 2012?'  :   'Meryl Streep',
            'Which movie won the oscar in 2000?'    :   'American Beauty',
            'When did Blanchett win an oscar for best actress?' :   '2014'
        }

        for q in qa.keys():
            print q
            wa = str(watson.answer(q))
            print '->', wa
            self.assertEqual(qa[q], wa)

    def test_alternate_samples(self):

        qa = {
            'Is Neeson an actor?'   :   'yes',
            'Did Jamie Foxx win the oscar for best actor in 2005?'   :   'yes',
            'Did Hathaway win an oscar in 2013?'    :   'yes',
            'Did Spielberg direct Schindler\'s List?'  :   'yes',
            'Did Meryl Streep won the oscar in 2012?'    :   'yes',
            'Which French actor win the oscar in 2012?' :   'Jean Dujardin',
            'Which movie with Neeson win the oscar for best film?'  :   'Schindler\'s List',
            'Where did Loren born?' :   'Pozzuoli, Italy',
            'When did Meryl Streep won the oscar for best actress?'  :   '1983',
            'Who directed Avengers: Age of Ultron?' :   'Joss Whedon'
        }

        for q in qa.keys():
            print q
            wa = str(watson.answer(q))
            print '->', wa
            self.assertEqual(qa[q], wa)

    def test_competition(self):

        qa = {
            'Did Neeson star in Schindler\'s List ?'    :   'yes',
            'Did Robertson star in Spider-Man 2?'   :   'no',
            'Is DiCaprio a director?'   :   'no',
            'Did De Niro win the oscar in 1981?'    :   'yes',
            # 'Is Boys Town by Taurog?'   :   'yes',    #wrong domain
            'Which actress won the oscar in 1999?'  :   'Gwyneth Paltrow',
            'When did Berry win an oscar for best actress?' :   '2002',
            'Who directed the best movie in 2014?'  :   'Steve McQueen',
            'Who directed Milk?' : 'Gus Van Sant',
            'Where maliza2@uic.edu signed in $100?' : 'I don\'t know'
        }

        for q in qa.keys():
            print q
            wa = str(watson.answer(q))
            print '->', wa
            self.assertEqual(qa[q], wa)


    def test_geography(self):

        qa = {
            'Is Rome the capital of Italy?' :   'yes',
            'Is France in Europe?'  :   'yes',
            'Is the Pacific deeper than the Atlantic?'  :   'yes',
            'Is the Indian deeper than the Arctic?' :   'yes',
            'In which continent does Canada lie?'   :   'North America',
            'With which countries does France have a border?'   :   'Italy',
            'Which is the highest mountain in the world?'   :   'Mount Everest',
            # 'Where is the highest mountain?',
            'Which is the deepest ocean?'   :   'Pacific Ocean'
        }

        for q in qa.keys():
            print q
            wa = str(watson.answer(q))
            print '->', wa
            self.assertEqual(qa[q], wa)



    def test_music(self):

        qa = {
            'Does the album Thriller include the track Beat It?'    :   'yes',
            'Does the track Beat It appears in the album Thriller?' :   'yes',
            'In which album does Aura appear?'  :   'Artpop',
            'Did Madonna sing Papa Do Not Preach?'  :   'yes',
            # 'Which pop artist sings Crazy In Love?' :   'Beyonce'   #wrong domain
            'Which album by Beyonce was released in 2014?'  :   '1989'
        }

        for q in qa.keys():
            print q
            wa = str(watson.answer(q))
            print '->', wa
            self.assertEqual(qa[q], wa)





