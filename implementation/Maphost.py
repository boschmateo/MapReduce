'''
@author: Jeroni Molina Mellado
@author: Roger Bosch Mateo
'''

from pyactor.context import set_context, create_host, serve_forever
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

if __name__ == "__main__":

    numberOfArguments = len(sys.argv)
    set_context()

    if (numberOfArguments == 2):
        host = create_host('http://127.0.0.1:'+sys.argv[1]+'/')
        registry = host.lookup_url('http://127.0.0.1:6000/registry', 'Registry','PublishSubscribe')
        registry.bindMapper(sys.argv[1], host)
    
    serve_forever()
