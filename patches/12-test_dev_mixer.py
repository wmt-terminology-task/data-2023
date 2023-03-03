#!/usr/bin/env python3

from sacremoses.tokenize import MosesDetokenizer
import argparse
import json
import os

os.makedirs("data/splits", exist_ok=True)

args = argparse.ArgumentParser()
args.add_argument("-l", "--lang", default="cs")
args = args.parse_args()

detokenize_cs = MosesDetokenizer(lang=args.lang).detokenize
detokenize_en = MosesDetokenizer(lang="en").detokenize

data_cs = [x.rstrip("\n") for x in open(f"data/clean_detok/{args.lang}-en.{args.lang}", "r").readlines()]
data_en = [x.rstrip("\n") for x in open(f"data/clean_detok/{args.lang}-en.en", "r").readlines()]
data_d1 = [json.loads(x) if len(x) > 1 else [] for x in open(f"data/clean_detok/{args.lang}-en.dict1.jsonl", "r").readlines()]
data_d2 = [json.loads(x) if len(x) > 1 else [] for x in open(f"data/clean_detok/{args.lang}-en.dict2.jsonl", "r").readlines()]

fout_cs = open(f"data/splits/dev.{args.lang}-en.{args.lang}", "w")
fout_en = open(f"data/splits/dev.{args.lang}-en.en", "w")
fout_d = open(f"data/splits/dev.{args.lang}-en.dict.jsonl", "w")

flipped = False

for sent_i, (sent_cs, sent_en, sent_d1, sent_d2) in enumerate(zip(data_cs, data_en, data_d1, data_d2)):
    if not sent_d1 or not sent_d2:
        continue

    if (((args.lang == "cs" and sent_i >= 662) or (args.lang == "de" and sent_i >= 621))
        and not flipped
    ):
        flipped = True
        fout_cs = open(f"data/splits/test.{args.lang}-en.{args.lang}", "w")
        fout_en = open(f"data/splits/test.{args.lang}-en.en", "w")
        fout_d = open(f"data/splits/test.{args.lang}-en.dict.jsonl", "w")

    # write in 3 modes
    fout_cs.write(sent_cs + "\n")
    fout_cs.write(sent_cs + "\n")
    fout_cs.write(sent_cs + "\n")
    fout_en.write(sent_en + "\n")
    fout_en.write(sent_en + "\n")
    fout_en.write(sent_en + "\n")
    fout_d.write("\n")
    fout_d.write(json.dumps(sent_d1, ensure_ascii=False) + "\n")
    fout_d.write(json.dumps(sent_d2, ensure_ascii=False) + "\n")