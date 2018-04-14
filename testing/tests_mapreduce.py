'''
@author: Jeroni Molina Mellado
@author: Roger Bosch Mateo
'''
import sys, time
import urllib2, re
import os.path
import unittest
from pyactor.context import set_context, create_host, Host, sleep, shutdown
from pyactor.exceptions import TimeoutError
from implementation.map import Map
from implementation.reduce import Reduce


class TestBasic(unittest.TestCase):
    def setUp(self):
        self.LOCALHOST="http://127.0.0.1"
        unittest.TestCase.setUp(self)
        set_context()

        self.host = create_host(self.LOCALHOST+":1679")

        self.reducer_host = create_host(self.LOCALHOST+":1277")
        self.mapper1_host = create_host(self.LOCALHOST+":1278")
        self.mapper2_host = create_host(self.LOCALHOST+":1279")

        self.reducer = host.lookup_url(self.LOCALHOST+':1277/', Host).spawn(1277, Reduce)
        self.mapper1 = host.lookup_url(self.LOCALHOST+':1278/', Host).spawn(1278, Map)
        self.mapper2 = host.lookup_url(self.LOCALHOST+':1279/', Host).spawn(1279, Map)

    def tearDown(self):
        shutdown()

    def test_1reducer(self):
        self.reducer.setNumberOfMappers(2)

        self.assertEqual(self.reducer.actor.nMappers, 2)
        self.assertEqual(self.reducer.actor.totalMappers, 0)
        self.assertEqual(self.reducer.actor.total, 0)

    def test_2mappers(self):
        self.mapper1.map("CW", self.LOCALHOST+":8000/0.part", self.reducer)
        self.mapper2.map("CW", self.LOCALHOST+":8000/1.part", self.reducer)




