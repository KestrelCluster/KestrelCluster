#!/bin/bash
# -*- mode: shell-script; indent-tabs-mode: nil; sh-basic-offset: 4; -*-
# ex: ts=8 sw=4 sts=4 et filetype=sh

installkernel() {
    instmods aufs
}

install() {
    inst_hook cmdline 30 "$moddir/parse-live.sh"
    inst_hook pre-udev 30 "$moddir/aufslive-genrules.sh"
    inst_hook pre-pivot 90 "$moddir/live-mount.sh"
}
