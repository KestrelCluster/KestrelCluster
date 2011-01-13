Dracut is a new initramfs infrastructure, very well designed and very efficient.

    http://fedoraproject.org/wiki/Dracut
    
    Ubuntu's casper or Debian's live-initramfs are great live modules for the
    initramfs-tools, but also are very complex, and designed with live cd in
    mind. 
    We don't need so much features, since our live nodes will have only a bunch
    of services, and we look for a simple and clean solution (KISS).
    
    
Download Dracut 007 :

   http://dracut.git.sourceforge.net/git/gitweb.cgi?p=dracut/dracut;a=snapshot;h=59a232ddcd1563362fd988037921dab9859042a3;sf=tgz

Create and install the debian package :

   tar -xzvf dracut-*.tar.gz
   pushd dracut-*/
   patch -p1 < ../dracut*.diff
   chmod 755 modules.d/90aufs-live/*
   dpkg-buildpackage -us -uc
   popd
   rm -R dracut-*/
   sudo dpkg -i dracut*.deb
