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

    #Reducer actor reference
    reducer = 0
    #Word count list
    wordCounting = dict()

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
        count = len(re.findall(r'\w+', contents))
        self.reducer.reduceCW(count)

    # Function that states the number of times a word appears in a file
    def wordCounting(self, address):
        #Get the file to read
        contents = urllib2.urlopen(address).readlines()
        for line in contents:
            line = re.sub( r'^\W+|\W+$', '', line )
            words = re.split( r'\W+', line )

            for word in words:
            	word=word.lower()
            	#If word exists
	            if (self.wordCounting.get(word)):
	                self.wordCounting[word] = self.wordCounting[word] + 1
	            #If it doesn't exist
	            else:
	                self.wordCounting[word] = 1

        self.reducer.reduceWC(self.wordCounting)


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

if __name__ == "__main__":
    set_context()

    #start execution time
    start_time = time.time()

    #Validate the entry argument length
    numberOfArguments = len(sys.argv)
    if (numberOfArguments != 3):
        print "python client.py <number of remote hosts> <mode>"
        exit(-1)

    remoteHostList = []
    numberOfSpawns = int(sys.argv[1])

    #Check if mode is correct
    mode = sys.argv[2]
    if ((mode != "CW") and (mode != "WC")):
        print "ERROR: Mode has to be CW (counting words) or WC (words count)"
        exit(-1)

    MIN_PORT_VALUE = 1277
    MAX_PORT_VALUE = MIN_PORT_VALUE + numberOfSpawns

    host = create_host('http://127.0.0.1:1679')

    #Spawn the reducer
    reducerHost = host.lookup_url('http://127.0.0.1:' + str(MAX_PORT_VALUE) + '/', Host)
    reducer = reducerHost.spawn(MAX_PORT_VALUE, 'client/Reduce')
    reducer.setNumberOfMappers(numberOfSpawns, host, start_time)

    #Spawn all the mappers
    for port in range(MIN_PORT_VALUE, MAX_PORT_VALUE):

        print "On port "+str(port)
        #Get the host reference
        remoteHost = host.lookup_url('http://127.0.0.1:' + str(port) + '/', Host)
        #Add the slaves into the list
        remoteHostList.append(remoteHost.spawn(port, 'client/Map'))

    #Testing the values
    for pos in range(numberOfSpawns):
        remoteHostList[pos].map(mode, "http://0.0.0.0:8000/" + str(pos) + ".part", reducer)
    
    shutdown()