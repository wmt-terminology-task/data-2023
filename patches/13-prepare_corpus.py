#!/usr/bin/env python3

import json
from nltk.tokenize import sent_tokenize

data = [json.loads(x) for x in open("data/ufal_corpus.jsonl", "r")]

fout = open("data/ufal_corpus_processed.jsonl", "w")

for line in data:
    if line["lang"] != "en":
        continue
    sents_cs = sent_tokenize(line["abstract_cs"], language="czech")
    sents_en = sent_tokenize(line["abstract_en"], language="english")
    if len(sents_cs) != len(sents_en):
        continue

    for sent_cs, sent_en in zip(sents_cs, sents_en):
        fout.write(json.dumps({"cs": sent_cs, "en": sent_en}, ensure_ascii=False)+ "\n")