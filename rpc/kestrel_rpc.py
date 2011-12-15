#!/usr/bin/env python

import os, sys, time, re
from daemon import Daemon
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler


def check_environ(key,default):
    try:
        return os.environ[key]
    except KeyError:
        return default


def check(variable,value,re):
    val=str(value)
    if re.match(val):
        return " " + variable + "=" + val
    else:
        raise Exception(" invalid " + variable + " = " + value)

num_re   = re.compile("[0-9]+")
true_re  = re.compile("True|False")
node_re  = re.compile(check_environ("node_re", "[0-9]+"))
group_re = re.compile(check_environ("group_re","[0-9A-Za-z_]+"))
image_re = re.compile(check_environ("image_re","[0-9A-Za-z_]+"))


class RequestHandler(SimpleXMLRPCRequestHandler):

    @classmethod
    def load_plugins(cls, plugin_dir):
        try:
            plugin_files = filter(lambda f:re.search('^plugin.*\.py',f),
                                    os.listdir(plugin_dir))
            # Make sure the files are sorted. This can be useful to set
            # priorities to plugins prefixing them with a number.
            plugin_files.sort()

            for plugin in plugin_files:
                d = {}
                execfile(os.path.join(plugin_dir,plugin), d)
                funcs = (filter(lambda f:f.startswith('kestrel_'),d))
                for func in funcs:
                    sys.stderr.write('Added function %s from plugin %s\n' % 
                                       (func, plugin))
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

    # Basic KestrelHPC methods
    #
    # It passes the action and the parameters to kestrel_daemon through the
    # FIFO file defined in KESTREL_RPC_FIFO

    def kestrel_connect(self, num_cpus, image):
        try:
            sys.stdout.write(" action=connect" + \
                             " ip=" + self.client_address[0] + \
                             check("cpu",   num_cpus, num_re) + \
                             check("image", image,    image_re ) )
            
            return time.strftime("%Y-%m-%d %H:%M:%S")
            
        except Exception as e:
            sys.stderr.write(" action=connect" + \
                             " ip=" + self.client_address[0] + str(e) )
            
            return "Invalid call"

    def kestrel_register(self, num_cpus, image, group):
        try:
            sys.stdout.write(" action=register" + \
                             " ip=" + self.client_address[0] + \
                             check("cpu",   num_cpus, num_re) + \
                             check("group", group,    group_re) + \
                             check("image", image,    image_re) )
            
            return time.strftime("%Y-%m-%d %H:%M:%S")
            
        except Exception as e:
            sys.stderr.write(" action=register" + \
                             " ip=" + self.client_address[0] + str(e))
            
            return "Invalid call"

    def kestrel_disconnect(self, reboot):
        try:
            sys.stdout.write(" action=disconnect " + \
                             " ip=" + self.client_address[0] + \
                             check("reboot", reboot, true_re) )
            
            return time.strftime("%Y-%m-%d %H:%M:%S")
            
        except Exception as e:
            sys.stderr.write(" action=disconnect " + \
                             " ip=" + self.client_address[0] + str(e))
            
            return "Invalid call"


plugins_dir = check_environ("KESTREL_RPC_PLUGINS", os.getcwd())
 
class MyDaemon(Daemon):
    def run(self):
        ip =          check_environ("FRONTEND_IP",      "localhost")
        port =    int(check_environ("KESTREL_RPC_PORT", "8000"))
        
        # Load the plugins from the plugin directory
        RequestHandler.load_plugins(plugins_dir)

        server = SimpleXMLRPCServer((ip, port), requestHandler=RequestHandler)
        server.serve_forever()


if __name__ == "__main__":
    user =    check_environ("KESTREL_USER",     None)
    fifo =    check_environ("KESTREL_RPC_FIFO", os.getcwd() + "/output")
    chroot =  check_environ("KESTREL_RPC_CHROOT",   None)
    
    if user is not None:
        pid_dir='/var/run/'
        log_dir='/var/log/'
    else:
        pid_dir=log_dir=os.getcwd()

    daemon = MyDaemon(pidfile= pid_dir + '/kestrel_rpc.py.pid',
                      stderr = log_dir + '/kestrel_rpc.log',
                      stdout = fifo,
                      user   = user,
                      chroot = chroot)

    if len(sys.argv) == 2:
        if '--start' == sys.argv[1]:
            daemon.start()
        elif '--stop' == sys.argv[1]:
            daemon.stop()
        else:
            sys.exit(2)

    else:
        daemon.start()

    sys.exit(0)
