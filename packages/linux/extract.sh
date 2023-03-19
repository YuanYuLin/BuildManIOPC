#!/bin/bash

DST_DIR=$1
#DIR="linux-6.1.19"
#DIR="linux-5.15.102"
DIR="linux-4.19.277"
TARBALL="$DIR.tar.xz"
tar Jxvf sources/$TARBALL -C $DST_DIR

cd $DST_DIR
ln -s $DIR linux

cd -
cp -v sources/$DIR.x86_64.config $DST_DIR/linux/.config
