#!/bin/sh
# -*- mode: shell-script; indent-tabs-mode: nil; sh-basic-offset: 4; -*-
# ex: ts=8 sw=4 sts=4 et filetype=sh

if [ -n "${root_persistence}" ]; then
    {
    printf 'KERNEL=="%s", SYMLINK+="livepersistence"\n' \
    	${root_persistence#/dev/} 
    printf 'SYMLINK=="%s", SYMLINK+="livepersistence"\n' \
	${root_persistence#/dev/} 
    } >> $UDEVRULESD/99-live-persistence-mount.rules

    echo '[ -e "/dev/livepersistence" ]' > $hookdir/initqueue/finished/livepersistence.sh
fi
