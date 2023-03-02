#!/usr/bin/bash

cat data/clean/cs-en.en | head -n $1 | tail -n 1
cat data/clean/cs-en.cs | head -n $1 | tail -n 1