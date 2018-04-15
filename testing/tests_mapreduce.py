'''
@author: Jeroni Molina Mellado
@author: Roger Bosch Mateo
'''
import sys, time
import os.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import urllib2, re
import unittest
from pyactor.context import set_context, create_host, Host, sleep, shutdown
from pyactor.exceptions import TimeoutError
from implementation.map import Map
from implementation.reduce import Reduce
from implementation.mapSequential import Map as SeqMap
from implementation.reduceSequential import Reduce as SeqReduce



class TestBasic(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        set_context()

        #localhost ip
        self.LOCALHOST="http://127.0.0.1"
        self.host = create_host(self.LOCALHOST+":1679")

        #Create 3 hosts
        self.reducer_host = create_host(self.LOCALHOST+":1277/")
        self.mapper1_host = create_host(self.LOCALHOST+":1278/")
        self.mapper2_host = create_host(self.LOCALHOST+":1279/")

        #Spawn 1 reducer and 2 mappers
        self.reducer = self.host.lookup_url(self.LOCALHOST+":1277/", Host).spawn(1277, Reduce)
        self.mapper1 = self.host.lookup_url(self.LOCALHOST+":1278/", Host).spawn(1278, Map)
        self.mapper2 = self.host.lookup_url(self.LOCALHOST+":1279/", Host).spawn(1279, Map)


    def tearDown(self):
        shutdown()

    def test_1wordcounting(self):
        #Set up reducer
        self.reducer.setNumberOfMappers(2)
        self.assertEqual(self.reducer.getNumberOfMappers(), 2)

        #Get mapper 1
        self.mapper1.map("WC", self.LOCALHOST+":8000/0.part", self.reducer)
        sleep(1)
        self.map1_dic = self.mapper1.getWC()

        #Get mapper 2
        self.mapper2.map("WC", self.LOCALHOST+":8000/1.part", self.reducer)
        sleep(1)
        self.map2_dic = self.mapper2.getWC()

        #Get the reducer
        sleep(3)
        self.red_dic = self.reducer.getWC()

        
        #Assert each word has de same count
        for word,count in self.red_dic.items():
            if (self.map1_dic.get(word)):
                count_map1 = self.map1_dic[word]
            else:
                count_map1 = 0

            if (self.map2_dic.get(word)):
                count_map2 = self.map2_dic[word]
            else:
                count_map2 = 0

            count_final = count_map2 + count_map1
            self.assertEqual(count, count_final)

    def test_2countingwords(self):
        #Set up reducer
        self.reducer.setNumberOfMappers(2)
        self.assertEqual(self.reducer.getNumberOfMappers(), 2)
        self.assertEqual(self.reducer.getCW(), 0)

        #Call mappers with counting words
        self.mapper1.map("CW", self.LOCALHOST+":8000/0.part", self.reducer)
        self.mapper2.map("CW", self.LOCALHOST+":8000/1.part", self.reducer)

        sleep(2)
        #Assert the result is correct
        self.red_count = self.reducer.getCW()
        self.assertEqual(self.red_count, (self.mapper1.getCW() + self.mapper2.getCW()))

    def test_3wordcountingcompare(self):
        #Set up reducer
        self.reducer.setNumberOfMappers(2)
        self.assertEqual(self.reducer.getNumberOfMappers(), 2)

        #Get mapper 1
        self.mapper1.map("WC", self.LOCALHOST+":8000/0.part", self.reducer)
        #Get mapper 2
        self.mapper2.map("WC", self.LOCALHOST+":8000/1.part", self.reducer)

        #Get the reducer
        sleep(3)
        self.red_dic = self.reducer.getWC()

        #Start a sequential map/reduce wit counting words
        seqReducer = SeqReduce()
        seqReducer.start()

        seqMapper= SeqMap()
        seqMapper.map("WC", "books/bible.txt", seqReducer)

        sleep(2)
        seqRed_dic = seqReducer.getWC()

        #Assert each word has been counted the same times
        for word,count in self.red_dic.items():
            self.assertEqual(count, seqRed_dic[word])

    def test_4countingwordscompare(self):
        #Set up reducer
        self.reducer.setNumberOfMappers(2)
        self.assertEqual(self.reducer.getNumberOfMappers(), 2)
        self.assertEqual(self.reducer.getCW(), 0)

        #Call mappers with counting words
        self.mapper1.map("CW", self.LOCALHOST+":8000/0.part", self.reducer)
        self.mapper2.map("CW", self.LOCALHOST+":8000/1.part", self.reducer)


        #Start a sequential map/reduce wit counting words
        seqReducer = SeqReduce()
        seqReducer.start()

        seqMapper= SeqMap()
        seqMapper.map("CW", "books/bible.txt", seqReducer)

        sleep(2)
        seqRed_count = seqReducer.getCW()
        sleep(2)
        self.assertEqual(self.reducer.getCW(), seqRed_count)
    

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    unittest.TextTestRunner(buffer=True).run(suite)



