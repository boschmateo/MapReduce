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

    host = create_host('http://192.168.1.37:1679')

    #Spawn the reducer
    reducerHost = host.lookup_url('http://192.168.1.37:' + str(1277) + '/', Host)
    reducer = reducerHost.spawn(1277, 'reduce/Reduce')
    reducer.setNumberOfMappers(numberOfSpawns)

    remoteHost = host.lookup_url('http://192.168.1.35:' + str(1278) + '/', Host)
    remoteHost = host.lookup_url('http://192.168.1.37:' + str(1279) + '/', Host)

    mac1_host = remoteHost.spawn(1278, 'map/Map')
    me1_host = remoteHost.spawn(1279, 'map/Map')

    mac1_host.map(mode, "http://192.168.1.37:8000/" + str(0) + ".part", reducer)
    me1_host.map(mode, "http://192.168.1.37:8000/" + str(1) + ".part", reducer)
    
    shutdown()