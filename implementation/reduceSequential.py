'''
@author: Jeroni Molina Mellado
@author: Roger Bosch Mateo
'''
import sys,time
import urllib2, re
import os.path

class Reduce(object):
    #StartTime
    start_time=0

    #Total of words for CW
    total=0
    #List of words for WC
    wordCounting = dict()

    # Function that obtain the results of the mappers, sum them and print it.
    def reduceCW(self, count):
        self.total = self.total + count
        print("The number of chracters is "+str(self.total)+"\n")
        #print execution time
        print("Execution time: %s seconds" % (time.time() - self.start_time))

    # Function that obtain the dictionaries of the mappers, agroup them and print the result.
    def reduceWC(self, wordDic):
        for word,count in wordDic.items():
            #If word exists
            if (self.wordCounting.get(word)):
                self.wordCounting[word] = self.wordCounting[word] + count
            #If it doesn't exist
            else:
                self.wordCounting[word] = count

        finish_time=time.time()
        
        for word,count in self.wordCounting.items():
            print (word+": "+str(count))
        #print execution time
        print("Execution time: %s seconds" % (finish_time - self.start_time))



    #This function must be called before starting mapping with the number of mappers
    def start(self):
        self.total=0
        self.start_time=time.time()

    # Getter of the total number of words
    def getCW(self):
        return self.total

    # Getter of the final dictionary
    def getWC(self):
        return self.wordCounting
