'''
@author: Jeroni Molina Mellado
@author: Roger Bosch Mateo
'''
import sys, time
import urllib2, re
import os.path
from pyactor.context import set_context, create_host, Host, sleep, shutdown
from pyactor.exceptions import TimeoutError

class Reduce(object):
    #Asynchronous
    _tell = ['reduceCW', 'reduceWC', 'setNumberOfMappers']
    _ref = ['setNumberOfMappers']

    mainHost = 0

    #Number of mappers finished
    nMappers=0
    #Number of mappers to expect
    totalMappers=0

    #StartTime
    start_time=0

    #Total of words for CW
    total=0
    #List of words for WC
    wordCounting = dict()

    def reduceCW(self, count):
        self.nMappers = self.nMappers + 1
        if ( self.nMappers < self.totalMappers):
            self.total= self.total + count
        elif (self.nMappers == self.totalMappers):
            self.total = self.total + count
            print("The number of chracters is "+str(self.total)+"\n")
            #print execution time
            print("Execution time: %s seconds" % (time.time() - self.start_time))

    def reduceWC(self, wordDic):
        self.nMappers = self.nMappers + 1
        if ( self.nMappers < self.totalMappers):
            for word,count in wordDic.items():
                #If word exists
                if (self.wordCounting.get(word)):
                    self.wordCounting[word] = self.wordCounting[word] + count
                #If it doesn't exist
                else:
                    self.wordCounting[word] = count

        elif (self.nMappers == self.totalMappers):
            for word,count in wordDic.items():
                #If word exists
                if (self.wordCounting.get(word)):
                    self.wordCounting[word] = self.wordCounting[word] + count
                #If it doesn't exist
                else:
                    self.wordCounting[word] = count

            for word,count in self.wordCounting.items():
                print (word+": "+str(count))
            #print execution time
            print("Execution time: %s seconds" % (time.time() - self.start_time))



    #This function must be called before starting mapping with the number of mappers
    def setNumberOfMappers(self, totalMappers, mainHost, start_time):
        self.mainHost=mainHost
        self.total=0
        self.nMappers=0
        self.totalMappers=totalMappers
        self.start_time=start_time