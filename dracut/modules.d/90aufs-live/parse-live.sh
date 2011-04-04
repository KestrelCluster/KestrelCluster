#!/bin/sh
# aufs live images are specified with
# aufslive root_persistence={LABEL|UUID|/dev/}=

if getarg aufslive; then
    aufslive=1
else
    return
fi

[ -z "$root_persistence" ] && root_persistence=$(getarg root_persistence=)

case "$root_persistence" in
    live:LABEL=*|LABEL=*)
	root_persistence="$(echo $root | sed 's,/,\\x2f,g')"
	root_persistence="live:/dev/disk/by-label/${root#LABEL=}"
        ;;
    live:CDLABEL=*|CDLABEL=*)
	root_persistence="$(echo $root | sed 's,/,\\x2f,g')"
	root_persistence="live:/dev/disk/by-label/${root#CDLABEL=}"
        ;;
    live:UUID=*|UUID=*)
	root_persistence="live:/dev/disk/by-uuid/${root#UUID=}"
        ;;
    live:/dev/*)
        ;;
    *)
        unset root_persistence
esac
info "AufsLive mode, root_persistence is now $root_persistence"
