#!/bin/bash

DST_DIR=$1
cd $DST_DIR
make ARCH=x86_64 -j5 V=1
