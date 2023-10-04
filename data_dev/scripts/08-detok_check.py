#!/usr/bin/env python3

from sacremoses.tokenize import MosesDetokenizer
import argparse
import json
import os

os.makedirs("data_dev/clean_detok", exist_ok=True)

args = argparse.ArgumentParser()
args.add_argument("-l", "--lang", default="cs")
args = args.parse_args()

detokenize_xx = MosesDetokenizer(lang=args.lang).detokenize
detokenize_en = MosesDetokenizer(lang="en").detokenize

data_xx = [x.rstrip("\n") for x in open(f"data_dev/clean/{args.lang}-en.{args.lang}", "r").readlines()]
data_en = [x.rstrip("\n") for x in open(f"data_dev/clean/{args.lang}-en.en", "r").readlines()]
data_d1 = [json.loads(x) if len(x) > 1 else [] for x in open(f"data_dev/clean/{args.lang}-en.dict1.jsonl", "r").readlines()]
data_d2 = [json.loads(x) if len(x) > 1 else [] for x in open(f"data_dev/clean/{args.lang}-en.dict2.jsonl", "r").readlines()]

fout_xx = open(f"data_dev/clean_detok/{args.lang}-en.{args.lang}", "w")
fout_en = open(f"data_dev/clean_detok/{args.lang}-en.en", "w")
fout_d1 = open(f"data_dev/clean_detok/{args.lang}-en.dict1.jsonl", "w")
fout_d2 = open(f"data_dev/clean_detok/{args.lang}-en.dict2.jsonl", "w")

for sent_i, (sent_xx, sent_en, sent_d1, sent_d2) in enumerate(zip(data_xx, data_en, data_d1, data_d2)):
    sent_xx_detok = detokenize_xx([sent_xx])
    sent_en_detok = detokenize_en([sent_en])
    sent_d1_detok = [{"en": detokenize_en([x["en"]]), args.lang: detokenize_xx([x[args.lang]])} for x in sent_d1]
    sent_d2_detok = [{"en": detokenize_en([x["en"]]), args.lang: detokenize_xx([x[args.lang]])} for x in sent_d2]

    # checks that the markables are included
    if not all(all(w in sent_en for w in x["en"].split()) for x in sent_d1):
        print(sent_en, sent_d1)

    if not all(all(w in sent_xx for w in x[args.lang].split()) for x in sent_d1):
        print(sent_xx, sent_d1)

    if not all(all(w in sent_en for w in x["en"].split()) for x in sent_d2):
        print(sent_en, sent_d2)

    if not all(all(w in sent_xx for w in x[args.lang].split()) for x in sent_d2):
        print(sent_xx, sent_d2)

    fout_xx.write(sent_xx_detok+"\n")
    fout_en.write(sent_en_detok+"\n")
    if sent_d1_detok:
        fout_d1.write(json.dumps(sent_d1_detok, ensure_ascii=False) + "\n")
    else:
        fout_d1.write("\n")

    if sent_d2_detok:
        fout_d2.write(json.dumps(sent_d2_detok, ensure_ascii=False) + "\n")
    else:
        fout_d2.write("\n")