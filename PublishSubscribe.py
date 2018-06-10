'''
@author: Roger Bosch Mateo
'''
import sys, time
import urllib2, re
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pyactor.context import set_context, create_host, Host, sleep, shutdown
from pyactor.exceptions import TimeoutError

class Registry(object):
    #Asynchronous
    _tell = ['bindReducer', 'bindMapper', 'unbind']
    _ref = ['bindReducer', 'bindMapper']
    _ask = []

    def __init__(self):
        self.mappers = {}
        self.reducer = ""
        self.reducerName = ""

    def bindReducer(self, name, actor):
        print "New reducer registerd ", name
        self.reducer = actor
        self.reducerName = name

    def bindMapper(self, name, actor):
        print "New mapper registered ", name
        self.mappers[name] = actor

    def unbind(self, name):
        if name in self.mappers.keys():
            del self.mappers[name]
        elif self.reducerName == name:
            self.reducer = ''

    def lookup(self, name):
        if name in self.mappers:
            return self.mappers[name]
        else:
            return None

    def splitFile(self, fileName, nFiles):
        os.system('./splitFile.sh '+str(nFiles))


    def mapreduce(self, mapClass, reduceClass, httpServer, fileName):
        #Split the file
        self.splitFile(fileName, len(self.mappers))

        #Spawn the reducer
        reducer = self.reducer.spawn(self.reducerName, reduceClass)

        #Spawn the mappers
        i=0
        for name,remoteHost in self.mappers.items():
            mapper = remoteHosts.spwan(name, mapClass)
            mapper.map(httpServer + '/' + str(i) + '.part', reducer)
            i = i + 1


if __name__ == "__main:__":

    IP_MASTER="127.0.0.1"

    set_context()

    host = create_host('http://127.0.0.1:6000/')

    registry = host.spawn('registry', Registry)

    serve_forever()