'''
@author: Jeroni Molina Mellado
@author: Roger Bosch Mateo
'''
import sys
from pyactor.context import set_context, create_host, Host, sleep, shutdown
from pyactor.exceptions import TimeoutError


class Server(object):
    #Synchronous (return method)
    _ask = ['reduce']
    #Asynchronous
    _tell = ['map', 'test']

    def map(self, function_to_apply, input_item):
        if (function_to_apply == 'CW'):
            countingWords(input_item)
        elif (function_to_apply == 'WC'):
            wordCounting(input_item)

    def test(self, value):
        print "I am "+str(value)

    def reduce(self, value):
        return value


if __name__ == "__main__":
    set_context()

    remoteHostList = []
    nSpawns=int(sys.argv[1])

    host = create_host('http://127.0.0.1:1679')

    #Spawn all the
    for x in range(1277, 1277+nSpawns):

        print "On port "+str(x)
        #Get the host reference
        remoteHost = host.lookup_url('http://127.0.0.1:'+str(x)+'/', Host)
        #Add the slaves into the list
        remoteHostList.append(remote_host.spawn(x, 'client/Server'))

    #Testing the values
    for x in range(nSpawns):
        remoteHostList[x].test(x)
    
    sleep(3)
    shutdown()
