#!/usr/bin/env python

import os, sys, time
from daemon import Daemon
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

class RequestHandler(SimpleXMLRPCRequestHandler):

    def _dispatch(self, method, params):
        try:
            func = getattr(self, 'kestrel_' + method)
        except AttributeError:
            raise Exception('method "%s" is not supported' % method)
        else:
            return func(*params)

    def kestrel_connect(self, num_cpus, image):
        sys.stdout.write(" action=connect" + \
                         " ip=" + self.client_address[0] + \
                         " cpu=" + str(num_cpus) + \
                         " image=" + str(image) )

        return time.strftime("%Y-%m-%d %H:%M:%S")

    def kestrel_register(self, num_cpus, image, group):
        sys.stdout.write(" action=register" + \
                         " ip=" + self.client_address[0] + \
                         " cpu=" + str(num_cpus) + 
                         " group=" + str(group) + \
                         " image=" + str(image) )

        return time.strftime("%Y-%m-%d %H:%M:%S")

    def kestrel_disconnect(self, reboot):
        sys.stdout.write(" action=disconnect " + \
                         " ip=" + self.client_address[0] + 
                         " reboot=" + str(reboot) )

        return time.strftime("%Y-%m-%d %H:%M:%S")

class MyDaemon(Daemon):
    def run(self):
        frontend_ip = os.environ["FRONTEND_IP"]
        port =    int(os.environ["KESTREL_RPC_PORT"])
        
        server = SimpleXMLRPCServer((frontend_ip, port),
                                    requestHandler=RequestHandler)
        server.serve_forever()


if __name__ == "__main__":

    daemon_path = os.environ["KESTREL_DATA_DIR"] + '/rpc/'

    daemon = MyDaemon(pidfile='/var/run/kestrel_rpc.py.pid',
                      stdout=daemon_path+'fifo',
                      stderr='/var/log/kestrel_rpc.log')
                      #chroot=daemon_path)
    daemon.start()
    sys.exit(0)
