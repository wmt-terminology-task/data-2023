#!/usr/bin/bash
mkdir -p data/align
mkdir -p data/align_small

BINFASTALIGN="/home/vilda/bin/fast_align/build/fast_align"
BINATOOLS="/home/vilda/bin/fast_align/build/atools"

cat data/tok/report.exp.de-en.de data/tok/CCAligned.de-en.de > data/align/de-en.de
cat data/tok/report.exp.de-en.en data/tok/CCAligned.de-en.en > data/align/de-en.en

cat data/tok/elitr.exp.cs-en.cs data/tok/CCAligned.cs-en.cs > data/align/cs-en.cs
cat data/tok/elitr.exp.cs-en.en data/tok/CCAligned.cs-en.en > data/align/cs-en.en

SPECIALDELIM=$'\001'
paste -d $SPECIALDELIM data/align/de-en.de data/align/de-en.en | sed "s/$SPECIALDELIM/ ||| /" > data/align/de-en.both
paste -d $SPECIALDELIM data/align/cs-en.cs data/align/cs-en.en | sed "s/$SPECIALDELIM/ ||| /" > data/align/cs-en.both

# no need to replace existing " ||| " with " || " (checked it's not in the data)

# cap to 10M
head -n 10000000 data/align/de-en.both | grep -ve "^ ||| $" > data/align/de-en.small
head -n 10000000 data/align/cs-en.both | grep -ve "^ ||| $" > data/align/cs-en.small

$BINFASTALIGN -i data/align/de-en.small -d -o -v > data/align/de-en.forward.align
$BINFASTALIGN -i data/align/de-en.small -d -o -v -r > data/align/de-en.reverse.align
$BINATOOLS -i data/align/de-en.forward.align -j data/align/de-en.reverse.align -c grow-diag-final-and > data/align/de-en.inters.align

$BINFASTALIGN -i data/align/cs-en.small -d -o -v > data/align/cs-en.forward.align
$BINFASTALIGN -i data/align/cs-en.small -d -o -v -r > data/align/cs-en.reverse.align
$BINATOOLS -i data/align/cs-en.forward.align -j data/align/cs-en.reverse.align -c grow-diag-final-and > data/align/cs-en.inters.align


for LANG in "de" "cs"; do
    head -n 1200 data/align/$LANG-en.small > data/align_small/$LANG-en.both
    head -n 1200 data/align/$LANG-en.inters.align > data/align_small/$LANG-en.algn
done