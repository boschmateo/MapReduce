'''
@author: Jeroni Molina Mellado
@author: Roger Bosch Mateo
'''
import sys, time
import urllib2, re
import os.path
from implementation.mapSequential import Map
from implementation.reduceSequential import Reduce

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
