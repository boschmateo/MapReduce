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

    IP_COMPUTER1="http://127.0.0.1"
    IP_COMPUTER2="http://127.0.0.1"

    host = create_host(IP_COMPUTER1+':1679')

    #Spawn the reducer
    reducerHost = host.lookup_url(IP_COMPUTER1 +':' + str(1277) + '/', Host)
    reducer = reducerHost.spawn(1277, 'reduce/Reduce')
    reducer.setNumberOfMappers(numberOfSpawns)

    remoteHost = host.lookup_url(IP_COMPUTER1 +':' + str(1278) + '/', Host)
    host1 = remoteHost.spawn(1278, 'map/Map')

    remoteHost = host.lookup_url(IP_COMPUTER2 +':' + str(1279) + '/', Host)
    host2 = remoteHost.spawn(1279, 'map/Map')

    # 8000 is the default port for the HTTP server
    host1.map(mode, IP_COMPUTER1+':8000/' + str(0) + ".part", reducer)
    host2.map(mode, IP_COMPUTER1+':8000/' + str(1) + ".part", reducer)
    
    shutdown()