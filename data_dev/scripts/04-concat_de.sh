#!/usr/bin/bash
mkdir -p data_dev/raw

head -n 600 ~/Downloads/de-en_{research,health}.txt/*.en > data_dev/raw/report.de-en.en
head -n 600 ~/Downloads/de-en_{research,health}.txt/*.de > data_dev/raw/report.de-en.de

wc -l data_dev/raw/report.de-en.*