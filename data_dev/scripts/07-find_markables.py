#!/usr/bin/env python3

import argparse

args = argparse.ArgumentParser()
args.add_argument("-f", "--file", default="data_dev/clean/cs-en.en")
args = args.parse_args()

data = [x.rstrip("\n").split(" ") for x in open(args.file, "r").readlines()]
markables = set()

for sent in data:
    # all capital words
    for word in sent:
        if all(c.isupper() for c in word) and len(word) >= 3:
            markables.add(word)

print("\n".join(markables))
print("Total:", len(markables))