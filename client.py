'''
@author: Jeroni Molina Mellado
@author: Roger Bosch Mateo
'''
from pyactor.context import set_context, create_host, Host, sleep, shutdown
from pyactor.exceptions import TimeoutError


class Server(object):
    #Synchronous (return method)
    _ask = ['reduce']
    #Asynchronous
    _tell = ['map']

    def map(self, funtion_to_apply, input_item):
        print "Map"

    def reduce(self, value):
        return value


if __name__ == "__main__":
    set_context()
    host = create_host('http://127.0.0.1:1679')

    remote_host = host.lookup_url('http://127.0.0.1:1277/', Host)
    slave = remote_host.spawn('slave', 'client/Server')
    slave2 = remote_host.spawn('slave2', 'client/Server')
    
    slave.map("function", "input")
    print slave2.reduce(4)
    print slave.reduce(3)

    sleep(3)
    shutdown()
