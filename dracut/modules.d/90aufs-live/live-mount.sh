#!/bin/sh

if [ -n "$aufslive" ]; then

   modprobe aufs

   mkdir /live
   mkdir /ro-root

   mount --move $NEWROOT /ro-root

   if [ -z "${root_persistence}" ]; then
      mount -t tmpfs -o rw,noatime,mode=755 tmpfs /live
   else
      mount -t auto -o rw,noatime /dev/livepersistence /live
   fi

   mount -t aufs -o noatime,dirs=/live=rw:/ro-root=rr aufs $NEWROOT

   for dir in live ro-root; do
      mkdir -p $NEWROOT/media/${dir}
      mount --move /${dir} $NEWROOT/media/${dir}
   done

fi
