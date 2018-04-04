'''
@author: Jeroni Molina Mellado
@author: Roger Bosch Mateo
'''
import sys, time
import urllib2, re
import os.path
from pyactor.context import set_context, create_host, Host, sleep, shutdown
from pyactor.exceptions import TimeoutError

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
    reducer = reducerHost.spawn(MAX_PORT_VALUE, 'reduce/Reduce')
    reducer.setNumberOfMappers(numberOfSpawns, host, start_time)

    #Spawn all the mappers
    for port in range(MIN_PORT_VALUE, MAX_PORT_VALUE):

        print "On port "+str(port)
        #Get the host reference
        remoteHost = host.lookup_url('http://127.0.0.1:' + str(port) + '/', Host)
        #Add the slaves into the list
        remoteHostList.append(remoteHost.spawn(port, 'map/Map'))

    #Testing the values
    for pos in range(numberOfSpawns):
        remoteHostList[pos].map(mode, "http://0.0.0.0:8000/" + str(pos) + ".part", reducer)
    
    shutdown()