#!/usr/bin/env python3

import nltk.tokenize
import json
import argparse
import random
random.seed(0)

sent_tokenize = nltk.tokenize.sent_tokenize

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

def align_markable(markable, sent_cs, sent_en):
    num_words = markable.count(" ") + 1
    translation_target = [] 
    alignment_targets_seen= set()

    for word_i in range(len(sent_en)):
        sent_trunk = " ".join(sent_en[word_i:])
        if sent_trunk.lower().startswith(markable.lower()):
            break
    assert sent_trunk.lower().startswith(markable.lower())

    alignment_targets_i_all = []
    for align_word_i in range(word_i, word_i+num_words):
        alignment_targets_i = [x[0] for x in align if x[1] == align_word_i and x[0] not in alignment_targets_seen]
        # remove prefix (Grand Prix - Velkou Velkou Cenu)
        alignment_targets_seen.update(alignment_targets_i)
        alignment_targets_i_all += alignment_targets_i
    
    # make sure that the mapped is a continuous segment from the CS side
    alignment_targets_i_all.sort()
    translation_target += [sent_cs[x] for x in alignment_targets_i_all]
        
    translation_target = " ".join(translation_target)
    translation_source = sent_trunk[:len(markable)]
    return translation_target, translation_source

data_both = [x.rstrip("\n").split(" ||| ") for x in open(f"data/align_small/{args.language}-en.both", "r").readlines()]
data_align = [x.rstrip("\n") for x in open(f"data/align_small/{args.language}-en.algn", "r").readlines()]

markables = set(open(f"data/markables/{args.language}-en.en", "r").read().rstrip().split("\n"))
# make sure we process longer markables first to avoid prefix issue
markables = sorted(list(markables), key=len, reverse=True)
markables = {x.lower() for x in markables}

fen = open(f"data/clean/{args.language}-en.en", "w")
fde = open(f"data/clean/{args.language}-en.{args.language}", "w")
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
    
    sents_en = sent_tokenize(sent_en)
    sents_cs = sent_tokenize(sent_cs)

    sent_cs = sent_cs.split(" ")
    sent_en = sent_en.split(" ")

    align = process_align_line(align)

    # x[0] is German/Czech, x[1] is English
    assert max([x[1] for x in align]) < len(sent_en) and max([x[0] for x in align]) < len(sent_cs)

    fen.write(" ".join(sent_en)+"\n")
    fde.write(" ".join(sent_cs)+"\n")

    # hacks for multi-word markables
    translation_dict_1 = []
    true_markables_length = []
    for word_i, word in enumerate(sent_en):
        sent_trunk = " ".join(sent_en[word_i:])
        sent_trunk_lower = " ".join(sent_en[word_i:]).lower()
        if any(sent_trunk_lower.startswith(markable) for markable in markables):
            # find the specific markable
            for markable in markables:
                if sent_trunk_lower.startswith(markable):
                    break

            translation_target, translation_source = align_markable(markable, sent_cs, sent_en)
            if len(translation_target) > 1 and len(translation_target)/len(translation_source) > 0.5 and len(translation_source)/len(translation_target) > 0.5:
                translation_dict_1.append({"en": translation_source, args.language: translation_target})
                true_markables_length.append(markable.count(" ") + 1)

    # add to output
    if len(translation_dict_1) > 0:
        fdict1.write(json.dumps(translation_dict_1, ensure_ascii=False) + "\n")
    else:
        fdict1.write("\n")
        
    # randomized dictionary
    translation_dict_2 = []
    markables_random_seen = set()
    for markable_len in true_markables_length:
        attempts = 20
        while True:
            markable_i = random.choice(range(len(sent_en)-markable_len+1))
            markable = " ".join(sent_en[markable_i:markable_i+markable_len])
            attempts -= 1
            if attempts == 0:
                break
            # disallow true markables
            if markable.lower() in markables:
                continue
            # disallow already added random markables
            if markable in markables_random_seen:
                continue
            markables_random_seen.add(markable)
            translation_target, translation_source = align_markable(markable, sent_cs, sent_en)
            print(markable, translation_target, translation_source, sent_en, sep=" ||| ")
            if len(translation_target) > 1 and len(translation_target)/len(translation_source) > 0.5 and len(translation_source)/len(translation_target) > 0.5:
                translation_dict_2.append({"en": translation_source, args.language: translation_target})
                break

    # add to output
    if len(translation_dict_2) > 0:
        fdict2.write(json.dumps(translation_dict_2, ensure_ascii=False) + "\n")
    else:
        fdict2.write("\n")
