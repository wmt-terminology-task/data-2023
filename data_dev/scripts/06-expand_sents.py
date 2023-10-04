#!/usr/bin/env python3

import nltk
import nltk.tokenize

data_0 = [x.rstrip("\n") for x in open("data_dev/raw/elitr.cs-en.cs", "r").readlines()]
data_1 = [x.rstrip("\n") for x in open("data_dev/raw/elitr.cs-en.en", "r").readlines()]

fout_0 = open("data_dev/raw/elitr.exp.cs-en.cs", "w")
fout_1 = open("data_dev/raw/elitr.exp.cs-en.en", "w")

for sent_0, sent_1 in zip(data_0, data_1):
    sents_0 = nltk.tokenize.sent_tokenize(sent_0, language="czech")
    sents_1 = nltk.tokenize.sent_tokenize(sent_1, language="english")
    if len(sents_0) != len(sents_1):
        sents_0 = [sent_0]
        sents_1 = [sent_1]

    for sent_0, sent_1 in zip(sents_0, sents_1):
        if (len(sent_0) < 4 and len(sent_1) < 4) or all(not x.isalpha() for x in sent_0) or all(not x.isalpha() for x in sent_1):
            continue
        fout_0.write(sent_0+"\n")
        fout_1.write(sent_1+"\n")



data_0 = [x.rstrip("\n") for x in open("data_dev/raw/report.de-en.de", "r").readlines()]
data_1 = [x.rstrip("\n") for x in open("data_dev/raw/report.de-en.en", "r").readlines()]

fout_0 = open("data_dev/raw/report.exp.de-en.de", "w")
fout_1 = open("data_dev/raw/report.exp.de-en.en", "w")

for sent_0, sent_1 in zip(data_0, data_1):
    sents_0 = nltk.tokenize.sent_tokenize(sent_0, language="german")
    sents_1 = nltk.tokenize.sent_tokenize(sent_1, language="english")
    if len(sents_0) != len(sents_1):
        sents_0 = [sent_0]
        sents_1 = [sent_1]
    for sent_0, sent_1 in zip(sents_0, sents_1):
        fout_0.write(sent_0+"\n")
        fout_1.write(sent_1+"\n")