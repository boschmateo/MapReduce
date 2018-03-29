'''
@author: Jeroni Molina Mellado
@author: Roger Bosch Mateo
'''
import sys
import urllib2, re
from pyactor.context import set_context, create_host, Host, sleep, shutdown
from pyactor.exceptions import TimeoutError

class Map(object):
    #Asynchronous
    _tell = ['map']
    _ref = ['map']

    reducer = 0

    def map(self, functionToCall, httpAddress, reducer):
        self.reducer = reducer
        if (functionToCall == 'CW'):
            self.countingWords(httpAddress)
        elif (functionToCall == 'WC'):
            self.wordCounting(httpAddress)

    #Counting words functions
    def countingWords(self, address):
        contents = urllib2.urlopen(address).read()
        count = len(re.findall(r'\w+', contents))
        self.reducer.reduce(count)

    def wordCounting(self, address):
        contents = urllib2.urlopen(address).readlines()

        for line in contents:
            line = re.sub( r'^\W+|\W+$', '', line )
            words = re.split( r'\W+', line )
            for word in words:
                word = word.lower()
                print '%s\t%s' % (word, 1)

class Reduce(object):
    #Asynchronous
    _tell = ['reduce', 'setNumberOfMappers']
    nMappers=0
    totalMappers=0
    total=0

    def reduce(self, count):
        self.nMappers = self.nMappers + 1
        if ( self.nMappers < self.totalMappers):
            self.total= self.total + count
        elif (self.nMappers == self.totalMappers):
            self.total = self.total + count
            print("The number of chracters is "+str(self.total))

    #This function must be called before starting mapping with the number of mappers
    def setNumberOfMappers(self, totalMappers):
        self.total=0
        self.nMappers=0
        self.totalMappers=totalMappers



if __name__ == "__main__":
    set_context()

    #Validate the entry argument length
    numberOfArguments = len(sys.argv)
    if (numberOfArguments != 2):
        print "python client.py <number of remote hosts>"
        exit(-1)

    remoteHostList = []
    numberOfSpawns = int(sys.argv[1])
    MIN_PORT_VALUE = 1277
    MAX_PORT_VALUE = MIN_PORT_VALUE + numberOfSpawns

    host = create_host('http://127.0.0.1:1679')

    #Spawn the reducer
    reducerHost = host.lookup_url('http://127.0.0.1:' + str(MAX_PORT_VALUE) + '/', Host)
    reducer = reducerHost.spawn(MAX_PORT_VALUE, 'client/Reduce')
    reducer.setNumberOfMappers(numberOfSpawns)

    #Spawn all the mappers
    for port in range(MIN_PORT_VALUE, MAX_PORT_VALUE):

        print "On port "+str(port)
        #Get the host reference
        remoteHost = host.lookup_url('http://127.0.0.1:' + str(port) + '/', Host)
        #Add the slaves into the list
        remoteHostList.append(remoteHost.spawn(port, 'client/Map'))

    #Testing the values
    for pos in range(numberOfSpawns):
        remoteHostList[pos].map("WC", "http://0.0.0.0:8000/client.py", reducer)
    

    sleep(3)
    shutdown()
