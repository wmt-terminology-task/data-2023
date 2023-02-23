#!/usr/bin/bash

cat ~/Downloads/doc_data/*c/src.txt > data/raw/elitr.cs-en.cs
cat ~/Downloads/doc_data/*c/ref.txt > data/raw/elitr.cs-en.en

wc -l data/raw/elitr.cs-en.*