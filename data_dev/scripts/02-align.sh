#!/usr/bin/bash
mkdir -p data_dev/align
mkdir -p data_dev/align_small

BINFASTALIGN="/home/vilda/bin/fast_align/build/fast_align"
BINATOOLS="/home/vilda/bin/fast_align/build/atools"

cat data_dev/tok/report.exp.de-en.de data_dev/tok/CCAligned.de-en.de > data_dev/align/de-en.de
cat data_dev/tok/report.exp.de-en.en data_dev/tok/CCAligned.de-en.en > data_dev/align/de-en.en
cat data_dev/tok/elitr.exp.cs-en.cs data_dev/tok/CCAligned.cs-en.cs > data_dev/align/cs-en.cs
cat data_dev/tok/elitr.exp.cs-en.en data_dev/tok/CCAligned.cs-en.en > data_dev/align/cs-en.en

SPECIALDELIM=$'\001'
paste -d $SPECIALDELIM data_dev/align/de-en.de data_dev/align/de-en.en | sed "s/$SPECIALDELIM/ ||| /" > data_dev/align/de-en.both
paste -d $SPECIALDELIM data_dev/align/cs-en.cs data_dev/align/cs-en.en | sed "s/$SPECIALDELIM/ ||| /" > data_dev/align/cs-en.both

# no need to replace existing " ||| " with " || " (checked it's not in the data)

# cap to 10M
head -n 10000000 data_dev/align/de-en.both | grep -ve "^ ||| $" > data_dev/align/de-en.small
head -n 10000000 data_dev/align/cs-en.both | grep -ve "^ ||| $" > data_dev/align/cs-en.small

$BINFASTALIGN -i data_dev/align/de-en.small -d -o -v > data_dev/align/de-en.forward.align
$BINFASTALIGN -i data_dev/align/de-en.small -d -o -v -r > data_dev/align/de-en.reverse.align
$BINATOOLS -i data_dev/align/de-en.forward.align -j data_dev/align/de-en.reverse.align -c grow-diag-final-and > data_dev/align/de-en.inters.align

$BINFASTALIGN -i data_dev/align/cs-en.small -d -o -v > data_dev/align/cs-en.forward.align
$BINFASTALIGN -i data_dev/align/cs-en.small -d -o -v -r > data_dev/align/cs-en.reverse.align
$BINATOOLS -i data_dev/align/cs-en.forward.align -j data_dev/align/cs-en.reverse.align -c grow-diag-final-and > data_dev/align/cs-en.inters.align

for LANG in "de" "cs"; do
    head -n 1200 data_dev/align/$LANG-en.small > data_dev/align_small/$LANG-en.both
    head -n 1200 data_dev/align/$LANG-en.inters.align > data_dev/align_small/$LANG-en.algn
done