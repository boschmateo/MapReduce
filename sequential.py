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

    def map(self, functionToCall, fileToRead, reducer):
	file = open(fileToRead, "r")
        self.reducer = reducer
        if (functionToCall == 'CW'):
            self.countingWords(file.read())
        elif (functionToCall == 'WC'):
            self.wordCounting(file.read())

    # Function that counts the number of words in a files
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

class Reduce(object):

    #StartTime
    start_time=0

    #Total of words for CW
    total=0
    #List of words for WC
    wordCounting = dict()

    def reduceCW(self, count):
	    self.total = self.total + count
	    print("The number of chracters is "+str(self.total)+"\n")
	    #print execution time
	    print("Execution time: %s seconds" % (time.time() - self.start_time))

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

if __name__ == "__main__":

    #Validate the entry argument length
    numberOfArguments = len(sys.argv)
    if (numberOfArguments != 3):
        print "python client.py <mode> <path to file>"
        exit(-1)

    
    #Check if mode is correct
    mode = sys.argv[1]
    if ((mode != "CW") and (mode != "WC")):
        print "ERROR: Mode has to be CW (counting words) or WC (words count)"
        exit(-1)

    reducer=Reduce()
    reducer.start()
    mapper=Map()
    mapper.map(mode, sys.argv[2], reducer)

   
