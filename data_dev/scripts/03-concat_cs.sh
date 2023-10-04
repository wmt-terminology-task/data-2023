#!/usr/bin/bash

cat ~/Downloads/doc_data_dev/*c/src.txt > data_dev/raw/elitr.cs-en.cs
cat ~/Downloads/doc_data_dev/*c/ref.txt > data_dev/raw/elitr.cs-en.en

wc -l data_dev/raw/elitr.cs-en.*