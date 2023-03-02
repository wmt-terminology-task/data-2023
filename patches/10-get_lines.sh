#!/usr/bin/bash

cat data/clean/de-en.en | head -n $1 | tail -n 1
cat data/clean/de-en.de | head -n $1 | tail -n 1