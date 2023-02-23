#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import json
import argparse
import random
random.seed(0)

args = argparse.ArgumentParser()
args.add_argument("-l", "--language", default="cs")
args = args.parse_args()

def process_align_line(align_txt):
    align_txt = [[int(y) for y in x.split("-")] for x in align_txt.split(" ")]
    return align_txt

def sent_filter(sent1, sent2):
    if "vilda" in sent1 or "vilda" in sent2:
        return False
    ratio = len(sent1.split())/len(sent1.split())
    if ratio < 0.5 or 1/ratio < 0.5:
        return False
    return True

data_both = [x.rstrip("\n").split(" ||| ") for x in open(f"data/align_small/{args.language}-en.both", "r").readlines()]
data_align = [x.rstrip("\n") for x in open(f"data/align_small/{args.language}-en.algn", "r").readlines()]

markables = set(open(f"data/markables/{args.language}-en.en", "r").read().rstrip().split("\n"))
markables = {x.lower() for x in markables}

fen = open(f"data/clean/{args.language}-en.en", "w")
fde = open(f"data/clean/{args.language}-en.de", "w")
fdict1 = open(f"data/clean/{args.language}-en.dict1.jsonl", "w")
fdict2 = open(f"data/clean/{args.language}-en.dict2.jsonl", "w")

seen_sents = set()

for (sent_cs, sent_en), align in zip(data_both, data_align):
    if not sent_filter(sent_cs, sent_en):
        continue
    if sent_cs in seen_sents or sent_en in seen_sents:
        continue
    seen_sents.add(sent_cs)
    seen_sents.add(sent_en)

    sent_cs = sent_cs.split(" ")
    sent_en = sent_en.split(" ")

    align = process_align_line(align)

    # x[0] is German/Czech, x[1] is English
    assert max([x[1] for x in align]) < len(sent_en) and max([x[0] for x in align]) < len(sent_cs)

    fen.write(" ".join(sent_en)+"\n")
    fde.write(" ".join(sent_cs)+"\n")

    # hacks for multi-word markables
    translation_dict_1 = []
    for word_i, word in enumerate(sent_en):
        sent_trunk = " ".join(sent_en[word_i:])
        sent_trunk_lower = " ".join(sent_en[word_i:]).lower()
        if any(sent_trunk_lower.startswith(markable) for markable in markables):
            # find the specific markable
            for markable in markables:
                if sent_trunk_lower.startswith(markable):
                    break

            num_words = markable.count(" ") + 1
            translation_target = [] 
            for align_word_i in range(word_i, word_i+num_words):
                alignment_targets_i = [x[0] for x in align if x[1] == align_word_i]
                translation_target += [sent_cs[x] for x in alignment_targets_i]
                
            translation_target = " ".join(translation_target)
            translation_source = sent_trunk[:len(markable)]
            if len(translation_target) > 1 and len(translation_target)/len(translation_source) > 0.5 and len(translation_target)/len(translation_source) < 2:
                translation_dict_1.append({"en": translation_source, args.language: translation_target})

    if len(translation_dict_1) > 0:
        fdict1.write(json.dumps(translation_dict_1, ensure_ascii=False) + "\n")
    else:
        fdict1.write("\n")
        
    # randomized dictionary
    translation_dict_2 = []
    words_i = random.sample(list(range(len(sent_en))), k=min(2, len(sent_en)))
    for word_i in words_i:
        markable = sent_en[word_i]
        sent_trunk = " ".join(sent_en[word_i:])
        num_words = 1
        translation_target = [] 
        for align_word_i in range(word_i, word_i+num_words):
            alignment_targets_i = [x[0] for x in align if x[1] == align_word_i]
            translation_target += [sent_cs[x] for x in alignment_targets_i]
            
        translation_target = " ".join(translation_target)
        translation_source = sent_trunk[:len(markable)]
        if len(translation_target) > 1 and len(translation_target)/len(translation_source) > 0.5 and len(translation_target)/len(translation_source) < 2:
            translation_dict_2.append({"en": translation_source, args.language: translation_target})

    if len(translation_dict_2) > 0:
        fdict2.write(json.dumps(translation_dict_2, ensure_ascii=False) + "\n")
    else:
        fdict2.write("\n")
