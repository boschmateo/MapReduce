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

class Reduce(object):
    #Asynchronous
    _tell = ['reduce','setNumberOfMappers']
    _ask = ['getNumberOfMappers', 'getResult', 'getWC']


    #Number of mappers finished
    nMappers=0
    #Number of mappers to expect
    totalMappers=0

    #StartTime
    start_time=0

    #Total of words for CW
    total=0

    # Function that obtain the results of the mappers, sum them and print it.
    def reduce(self, count):
        self.nMappers = self.nMappers + 1
        if ( self.nMappers < self.totalMappers):
            self.total= self.total + count
        elif (self.nMappers == self.totalMappers):
            self.total = self.total + count
            print("The number of chracters is "+str(self.total)+"\n")
            #print execution time
            print("Execution time: %s seconds" % (time.time() - self.start_time))


    # Function that initialitate the reduce
    # This function must be called before starting mapping with the number of mappers
    def setNumberOfMappers(self, totalMappers):
        self.total=0
        self.nMappers=0
        self.totalMappers=totalMappers
        self.start_time=time.time()

    # Getter of the number of mappers
    def getNumberOfMappers(self):
        return self.totalMappers

    # Getter of the total number of words
    def getResult(self):
        return self.total