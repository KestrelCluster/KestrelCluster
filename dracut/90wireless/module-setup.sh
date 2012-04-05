#!/bin/bash
# -*- mode: shell-script; indent-tabs-mode: nil; sh-basic-offset: 4; -*-
# ex: ts=8 sw=4 sts=4 et filetype=sh

depends() {
    # We depend on network modules being loaded
    echo network
}

installkernel() {
    for modname in $(find "$srcmods/kernel/drivers/net/wireless" \
                          "$srcmods/kernel/net/wireless" \
                          -name '*.ko' 2>/dev/null); do
    	instmods $modname
    done
}

install() {
    inst iwconfig
    inst wpa_supplicant
    inst ifconfig
    inst ping
    
    inst "$moddir/wireless" "/sbin/wireless"
    inst_hook cmdline 20 "$moddir/parse-wireless.sh"
    inst_hook pre-udev 20 "$moddir/wireless-genrules.sh"
}

