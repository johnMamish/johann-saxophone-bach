#!/bin/bash

for file in ./bach-371-chorales/kern/* ; do
    extension="${file##*.}"
    temp="${file%.*}"
    name="${temp##*/}"
    outpath="transposed/"
    fileout=$outpath$name
    python convert.py $file $fileout
done
