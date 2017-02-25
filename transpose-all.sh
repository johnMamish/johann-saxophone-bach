#!/bin/bash

for file in ./bach-371-chorales/kern/* ; do
    extension="${file##*.}"
    temp="${file%.*}"
    name="${temp##*/}"
    outpath="bach-minus-two-semitones/"
    fileout=$outpath$name
    mkdir $outpath
    python convert.py $file $fileout
    rm $fileout    #2 files are produced: $fileout and $fileout.pdf.  We only want the pdf.
done
