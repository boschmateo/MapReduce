'''
@author: Jeroni Molina Mellado
@author: Roger Bosch Mateo
'''
import sys, time
import urllib2, re
import os.path

class Map(object):
    #Asynchronous

    #Reducer actor reference
    reducer = 0
    #Word count list
    wordDic = dict()

    # Main function that allows to map a file seqcuentally by counting the number of words(CW)
    # or by counting each word appereance.
    # Usage:
    #   functionToCall: "CW" or "WC"
    #   fileToRead:     Directory of the file
    #   reducer:        reducer actor reference
    def map(self, functionToCall, fileToRead, reducer):
        file = open(fileToRead, "r")
        self.reducer = reducer
        if (functionToCall == 'CW'):
            self.countingWords(file.read())
        elif (functionToCall == 'WC'):
            self.wordCounting(file.read())

    # Function that counts the number of words in a file
    def countingWords(self, inputData):
        count = len(re.findall(r'\w+', inputData))
        self.reducer.reduceCW(count)

    # Function that states the number of times a word appears in a file
    def wordCounting(self, inputData):
        #Get the file to read
        inputData = inputData.decode('utf_8')
        words = re.compile(r"[a-zA-Z]+").findall(inputData)

        for word in words:
            word=word.lower()
            #If word exists
            if (self.wordDic.get(word)):
                self.wordDic[word] = self.wordDic[word] + 1
            #If it doesn't exist
            else:
                self.wordDic[word] = 1
        self.reducer.reduceWC(self.wordDic)

    # Getter of the number of words
    def getCW(self):
        return self.count
    # Getter of the dictionary
    def getWC(self):
        return self.wordDic