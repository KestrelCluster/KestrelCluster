#!/bin/sh
# -*- mode: shell-script; indent-tabs-mode: nil; sh-basic-offset: 4; -*-
# ex: ts=8 sw=4 sts=4 et filetype=sh

essid=$(getarg rd_essid=)
proto=$(getarg rd_proto=)
pass=$(getarg rd_pass=)

{
echo "essid=$essid"
echo "proto=$proto"
echo "pass=$pass"
} > /tmp/wireless.info
