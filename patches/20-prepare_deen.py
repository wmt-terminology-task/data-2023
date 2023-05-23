#!/usr/bin/env python3

import glob
import os
from mosestokenizer import MosesSentenceSplitter
import json
import chardet

# https://muchmore.dfki.de/resources1.htm

sentence_splitter_en = MosesSentenceSplitter(lang="en")
sentence_splitter_de = MosesSentenceSplitter(lang="de")

fout = open("data/muchmore_corpus.jsonl", "w")

for fde in glob.glob("data/springer_german_train_plain/*.abstr"):
    fen = fde.replace(".ger.", ".eng.").replace("_german_", "_english_")
    if not os.path.exists(fen):
        continue
    dataen = chardet.detect(open(fen, "rb").read())
    dataen = open(fen, "r", encoding=dataen["encoding"]).read().strip()
    datade = chardet.detect(open(fde, "rb").read())
    datade = open(fde, "r", encoding=datade["encoding"]).read().strip()

    dataen = sentence_splitter_en([dataen])
    datade = sentence_splitter_de([datade])
    if len(dataen) != len(datade):
        continue

    for senten, sentde in zip(dataen, datade):
        # check lengths
        if len(senten) < 20:
            continue
        ratio = len(senten.split())/len(sentde.split())
        if ratio > 1.5 or ratio < 0.5:
            continue
        fout.write(json.dumps({"en": senten, "de": sentde}, ensure_ascii=False) +"\n")