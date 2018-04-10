'''
@author: Jeroni Molina Mellado
@author: Roger Bosch Mateo
'''

from pyactor.context import set_context, create_host, serve_forever
import sys

if __name__ == "__main__":

    numberOfArguments = len(sys.argv)
    set_context()

    if (numberOfArguments == 2):
        host = create_host('http://192.168.1.33:'+sys.argv[1]+'/')
        print 'host listening at port '+sys.argv[1]
    else:
        print "****You are currently only running one host****"
        host = create_host('http://192.168.1.33:1277/')
        print 'host listening at port 1277'
    
    serve_forever()
