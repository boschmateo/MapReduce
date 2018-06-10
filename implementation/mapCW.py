'''
@author: Jeroni Molina Mellado
@author: Roger Bosch Mateo
'''
import sys, time
import urllib2, re
import os.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pyactor.context import set_context, create_host, Host, sleep, shutdown
from pyactor.exceptions import TimeoutError

class Map(object):
    #Asynchronous
    _tell = ['map']
    _ref = ['map']
    _ask = ['getResult']

    #Count
    count = 0

    # Function that counts the number of words in a files
    def map(self, address, reducer):
        contents = urllib2.urlopen(address).read()
        self.count = len(re.findall(r'\w+', contents))
        reducer.reduce(self.count)

    # Getter of the number of words
    def getResult(self):
        return self.count