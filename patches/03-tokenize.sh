#!/usr/bin/bash

for LANG in "cs" "de" "en"; do
for file in data/raw/*.$LANG; do
    echo $file
    fout="${file/\/raw\//\/tok\/}"
    sacremoses -l $LANG -j 20 tokenize < $file > $fout
done
done