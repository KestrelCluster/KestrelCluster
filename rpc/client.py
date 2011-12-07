#!/usr/bin/env python

import os, sys, xmlrpclib, socket

print "KestrelHPC RPC debugging util"

try:
    s = xmlrpclib.ServerProxy("http://localhost:8000")

    if not os.path.exists("output"):
        print "Output file not found: Start kestrel_rpc.py"
        sys.exit(1)
    
    # Clear output's contents
    f = open('output', 'w')
    f.write('')
    f.close()
    
    # Open KestrelHPC RPC's output file
    f = open('output', 'r')
    
    print 
    print "Method: register"
    print "\tresponse : \"" + s.register("2", "image1", "group1") + "\""
    print "\tserver output : \"" + f.readline() + "\""
    print
    print "Method: connect"
    print "\tresponse : \"" + s.connect("2", "image1") + "\""
    print "\tserver output : \"" + f.readline() + "\""
    print
    print "Method: disconnect"
    print "\tresponse : \"" + s.disconnect(True) + "\""
    print "\tserver output : \"" + f.readline() + "\""
    print
    print "Method: sample"
    print "\tresponse : \"" + s.sample("Testing plugins") + "\""
    print "\tserver output : \"" + f.readline()
    print
    f.close()

except socket.error:
    print "Could not find server. Start kestrel_rpc.py"
    sys.exit(1)

# Clear output's contents
f = open('output', 'w')
f.write('')
f.close()
