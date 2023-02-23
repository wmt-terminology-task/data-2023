#!/usr/bin/bash

head -n 600 ~/Downloads/de-en_{research,health}.txt/*.en > data/raw/report.de-en.en
head -n 600 ~/Downloads/de-en_{research,health}.txt/*.de > data/raw/report.de-en.de

wc -l data/raw/report.de-en.*