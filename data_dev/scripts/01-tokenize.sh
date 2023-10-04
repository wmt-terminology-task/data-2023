#!/usr/bin/bash

# 
# Tokenize raw dev files.
# 

for LANG in "cs" "de" "en"; do
for file in data_dev/raw/*.$LANG; do
    echo $file
    fout="${file/\/raw\//\/tok\/}"
    sacremoses -l $LANG -j 20 tokenize < $file > $fout
    # remove line breaks
    sed -i "s/\w- //g" $fout
done
done