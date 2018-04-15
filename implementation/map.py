'''
@author: Jeroni Molina Mellado
@author: Roger Bosch Mateo
'''
import sys, time
import urllib2, re
import os.path
from pyactor.context import set_context, create_host, Host, sleep, shutdown
from pyactor.exceptions import TimeoutError

class Map(object):
    #Asynchronous
    _tell = ['map']
    _ref = ['map']
    _ask = ['getCW', 'getWC']

    #Reducer actor reference
    reducer = 0
    #Word count list
    wordDic = dict()
    #Count
    count = 0

    # Main function that allows to map a file by counting the number of words(CW)
    # or by counting each word appereance.
    # Usage:
    #   functionToCall: "CW" or "WC"
    #   httpAddress:    Address for the file
    #   reducer:        reducer actor reference
    def map(self, functionToCall, httpAddress, reducer):
        self.reducer = reducer
        if (functionToCall == 'CW'):
            self.countingWords(httpAddress)
        elif (functionToCall == 'WC'):
            self.wordCounting(httpAddress)

    # Function that counts the number of words in a files
    def countingWords(self, address):
        contents = urllib2.urlopen(address).read()
        self.count = len(re.findall(r'\w+', contents))
        self.reducer.reduceCW(self.count)

    # Function that states the number of times a word appears in a file
    def wordCounting(self, address):
        #Get the file to read
        contents = urllib2.urlopen(address).readlines()
        for line in contents:
            line = line.decode('utf_8')
            words = re.compile(r"[a-zA-Z]+").findall(line)


            for word in words:
                word=word.lower()
                #If word exists
                if (self.wordDic.get(word)):
                    self.wordDic[word] = self.wordDic[word] + 1
                #If it doesn't exist
                else:
                    self.wordDic[word] = 1
    
        self.reducer.reduceWC(self.wordDic)

    def getCW(self):
        return self.count

    def getWC(self):
        return self.wordDic