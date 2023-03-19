#!/bin/bash

DST_DIR=$1
DIR="x86-64--glibc--stable-2022.08-1"
TARBALL="$DIR.tar.bz2"
tar jxvf sources/$TARBALL -C $DST_DIR
cd $DST_DIR
ln -s $DIR toolchains

