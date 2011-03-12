#!/usr/bin/env python

import os, sys, time
from daemon import Daemon
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from os.path import join as pj

class RequestHandler(SimpleXMLRPCRequestHandler):

    @classmethod
    def load_plugins(cls, plugin_dir):
        try:
            plugin_files = filter(lambda f:f.endswith('.py'),
                                    os.listdir(plugin_dir))
            # Make sure the files are sorted. This can be useful to set
            # priorities to plugins prefixing them with a number.
            plugin_files.sort()

            for plugin in plugin_files:
                d = {}
                execfile(pj(plugin_dir,plugin), d)
                funcs = (filter(lambda f:f.startswith('kestrel_'),d))
                for func in funcs:
                    sys.stderr.write('Added function %s from plugin %s'%(func, plugin))
                    setattr(cls, func, d[func])

        except OSError:
            sys.stderr.write('Warning: Plugin directory not found. Skipping.\n')

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
        plugins_dir = os.environ["KESTREL_RPC_PLUGINS"]

        # Load the plugins from the plugin directory
        RequestHandler.load_plugins(plugins_dir)

        server = SimpleXMLRPCServer((frontend_ip, port),
                                    requestHandler=RequestHandler)
        server.serve_forever()


if __name__ == "__main__":
    daemon_path = os.environ["KESTREL_RPC_DIR"]
    fifo =        os.environ["KESTREL_RPC_FIFO"]

    daemon = MyDaemon(pidfile='/var/run/kestrel_rpc.py.pid',
                      stdout=fifo,
                      stderr='/var/log/kestrel_rpc.log')
                      #chroot=daemon_path)

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        else:
            sys.exit(2)

    else:
        daemon.start()

    sys.exit(0)
