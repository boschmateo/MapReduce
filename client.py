'''
@author: Jeroni Molina Mellado
@author: Roger Bosch Mateo
'''
import sys
import urllib2, re
from pyactor.context import set_context, create_host, Host, sleep, shutdown
from pyactor.exceptions import TimeoutError


class Server(object):
    #Synchronous (return method)
    _ask = ['reduce']
    #Asynchronous
    _tell = ['map', 'test']

    # Allows to map an input file from an HTTP address
    # Mapping can be done in 2 ways:
    #       -CW: counting the number of words
    #       -WC: counting the appearance of each word
    def map(self, functionToCall, httpAddress):
        if (functionToCall == 'CW'):
            countingWords(httpAddress)
        elif (functionToCall == 'WC'):
            wordCounting(httpAddress)

    # Allows to reduce the input as desired        
    def reduce(self, value):
        #TODO: Distinguish between CW and WC
        return value

    #Just for testing, this will be deleted
    def test(self, value):
        print "I am " + str(value)

    #Counting words functions
    def countingWords(self, address):
        contents = urllib2.urlopen(address).read()
        count = len(re.findall(r'\w+', contents))
        print (count)


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

    #Spawn all the
    for port in range(MIN_PORT_VALUE, MAX_PORT_VALUE):

        print "On port "+str(port)
        #Get the host reference
        remoteHost = host.lookup_url('http://127.0.0.1:' + str(port) + '/', Host)
        #Add the slaves into the list
        remoteHostList.append(remote_host.spawn(port, 'client/Server'))

    #Testing the values
    for pos in range(numberOfSpawns):
        remoteHostList[pos].test(pos)
    

    sleep(3)
    shutdown()
