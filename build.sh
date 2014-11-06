#!/bin/sh

whereami=$(dirname $0)
readonly TOPDIR=`rpm --eval '%{_topdir}'`

if [ ! -f "/etc/rpm/macros.dist" ] && \
   [ ! -f "/etc/rpm/macros.disttag" ];   then echo "please install 'buildsys-macros' rpm and try again" ; exit 1 ; fi
if [ ! -f "$(which rpmbuild)" ];         then echo "please install 'rpm-build' rpm and try again" ; exit 1 ; fi
if [ ! -f "$(which spectool)" ];         then echo "please install 'rpmdevtools' rpm and try again" ; exit 1 ; fi
if [ ! -f "$(which rpmdev-setuptree)" ]; then echo "please install 'rpmdevtools' rpm and try again" ; exit 1 ; fi

# creates build tree
/usr/bin/rpmdev-setuptree

cp -f ${whereami}/runit.spec $TOPDIR/SPECS/
cp -f ${whereami}/*.patch    $TOPDIR/SOURCES/
cp -f ${whereami}/{1,2,3}    $TOPDIR/SOURCES/
cp -f ${whereami}/runit.init $TOPDIR/SOURCES/
cp -f ${whereami}/runsvdir-start.service    $TOPDIR/SOURCES/
/usr/bin/spectool -C $TOPDIR/SOURCES/ -g ${whereami}/runit.spec 

rpmbuild -bb $TOPDIR/SPECS/runit.spec
