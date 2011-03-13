#!/usr/bin/env python

import sys

def kestrel_plugin_sample(self, test):
    
    sys.stdout.write("received : " + test)

    return "It works :-)"
