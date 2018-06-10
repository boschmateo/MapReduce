'''
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

    #Word count list
    wordDic = dict()

    # Function that states the number of times a word appears in a file
    def map(self, address, reducer):
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
    
        reducer.reduceWC(self.wordDic)

    # Getter of the number of words
    def getResult(self):
        return self.wordDic