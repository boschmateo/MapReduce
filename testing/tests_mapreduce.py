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


class TestBasic(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        set_context()

        self.LOCALHOST="http://127.0.0.1"
        self.host = create_host(self.LOCALHOST+":1679")

        self.reducer_host = create_host(self.LOCALHOST+":1277/")
        self.mapper1_host = create_host(self.LOCALHOST+":1278/")
        self.mapper2_host = create_host(self.LOCALHOST+":1279/")

        self.reducer = self.host.lookup_url(self.LOCALHOST+":1277/", Host).spawn(1277, Reduce)
        self.mapper1 = self.host.lookup_url(self.LOCALHOST+":1278/", Host).spawn(1278, Map)
        self.mapper2 = self.host.lookup_url(self.LOCALHOST+":1279/", Host).spawn(1279, Map)

    def tearDown(self):
        shutdown()

    def test_1countingwords(self):
        self.reducer.setNumberOfMappers(2)
        self.assertEqual(self.reducer.getNumberOfMappers(), 2)
        self.assertEqual(self.reducer.getCW(), 0)

        self.mapper1.map("CW", self.LOCALHOST+":8000/0.part", self.reducer)
        self.mapper2.map("CW", self.LOCALHOST+":8000/1.part", self.reducer)
        sleep(2)
        self.assertEqual(self.reducer.getCW(), (self.mapper1.getCW() + self.mapper2.getCW()))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)



