#!/bin/sh

# Don't continue if we don't need wireless
[ -z "$essid" ] && return;


printf 'ACTION=="add", SUBSYSTEM=="net", ENV{DEVTYPE}=="wlan", RUN:="/sbin/wireless $env{INTERFACE}"\n' \
    > /etc/udev/rules.d/10-wireless.rules
