#!/usr/bin/env python3

import nltk
import nltk.tokenize
import argparse

args = argparse.ArgumentParser()
args.add_argument("-f", "--file", default="data/clean/cs-en.en")
args = args.parse_args()

data = [x.rstrip("\n").split(" ") for x in open(args.file, "r").readlines()]

markables = set()
# for sent in data:
    # # strip first word
    # sent = sent[1:]
    # capitals = [x[0].isupper() or x == "&amp;" for x in sent]
    # last_i = 0
    # for start_i in range(len(sent)-1):
    #     while True:
    #         last_i += 1
    #         if not all(x for x in capitals[start_i:last_i]) or last_i >= len(sent):
    #             break

    #     markable = " ".join(sent[start_i:last_i-1])
    #     if last_i >= start_i+3 and all(x for x in capitals[start_i:last_i-1]) and len(markable) >= 4:
    #         markables.add(markable)


for sent in data:
    # all capital words
    for word in sent:
        if all(c.isupper() for c in word) and len(word) >= 3:
            markables.add(word)

print("\n".join(markables))
print("Total:", len(markables))