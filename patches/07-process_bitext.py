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
    ratio = len(sent1.split())/len(sent2.split())
    if ratio < 0.5 or 1/ratio < 0.5:
        return False
    sent1_alphas = len([x for x in sent1 if x.isalpha()])
    sent2_alphas = len([x for x in sent2 if x.isalpha()])
    sent1_spaces = len([x for x in sent1 if x == " "])
    sent2_spaces = len([x for x in sent2 if x == " "])
    if sent1_alphas <= 2 or sent2_alphas <= 2:
        return False
    if sent1_spaces >= 0.8*sent1_alphas or sent2_spaces >= 0.8*sent2_alphas:
        return False
    # if not sent1[0].isupper() or not sent2[0].isupper():
    #     return False
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

def mutate_markables_1(translation_source, translation_target, data_fix):
    possible_match = [x for x in data_fix if translation_target == x[0]]
    assert len(possible_match) <= 1
    if possible_match:
        possible_match = possible_match[0]
        if possible_match[1] == "DEL":
            return None, None
        if possible_match[1] == "OTHER":
            return possible_match[2], translation_target
        if possible_match[1] == "SELF":
            return translation_source, possible_match[2]

    possible_match = [x for x in data_fix if translation_source == x[0]]
    assert len(possible_match) <= 1
    if possible_match:
        possible_match = possible_match[0]
        if possible_match[1] == "DEL":
            return None, None
        if possible_match[1] == "OTHER":
            return translation_source, possible_match[2]
        if possible_match[1] == "SELF":
            return possible_match[2], translation_target

    possible_match = [x for x in data_fix if translation_source + " + " + translation_target == x[0]]
    assert len(possible_match) <= 1
    if possible_match:
        possible_match = possible_match[0]
        if possible_match[1] == "DEL":
            return None, None
        if possible_match[1] == "ALL":
            return possible_match[2].split(" + ")

    # fallback with noop
    return translation_source, translation_target

data_both = [x.rstrip("\n").split(" ||| ") for x in open(f"data/align_small/{args.language}-en.both", "r").readlines()]
data_align = [x.rstrip("\n") for x in open(f"data/align_small/{args.language}-en.algn", "r").readlines()]

data_fix1 = [x.rstrip("\n").split(" |") for x in open(f"data/markables/{args.language}-en.fix1", "r").readlines()]
data_fix1 = [tuple([x[0]]+ x[1].split("| ")) for x in data_fix1]
data_fix2 = [x[1:].rstrip("\n").split(" | ") for x in open(f"data/markables/{args.language}-en.fix2", "r").readlines()]
data_fix2 = [(int(x[0]), *tuple(x[1].split(" + "))) for x in data_fix2]
markables = set(open(f"data/markables/{args.language}-en.en", "r").read().rstrip().split("\n"))
# make sure we process longer markables first to avoid substring issue
markables = sorted(list(markables), key=len, reverse=True)
markables = {x.lower() for x in markables if x}

fen = open(f"data/clean/{args.language}-en.en", "w")
fde = open(f"data/clean/{args.language}-en.{args.language}", "w")
fdict1 = open(f"data/clean/{args.language}-en.dict1.jsonl", "w")
fdict2 = open(f"data/clean/{args.language}-en.dict2.jsonl", "w")

seen_sents = set()
processed_sents = 0

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
    markables_seen = set()
    for word_i, word in enumerate(sent_en):
        sent_trunk = " ".join(sent_en[word_i:])
        sent_trunk_lower = " ".join(sent_en[word_i:]).lower()
        if any(sent_trunk_lower.startswith(markable) for markable in markables):
            # find the specific markable
            for markable in markables:
                if sent_trunk_lower.startswith(markable):
                    break


            translation_target, translation_source = align_markable(markable, sent_cs, sent_en)
            translation_source, translation_target = mutate_markables_1(translation_source, translation_target, data_fix1)
            # TODO: check that the mutations appear in source and target
            if not translation_source:
                continue
            if (
                len(translation_target) > 1 and
                len(translation_target)/len(translation_source) > 0.5 and
                len(translation_source)/len(translation_target) > 0.5 and
                translation_source not in markables_seen and
                translation_target not in markables_seen
            ):
                markables_seen.add(translation_source)
                markables_seen.add(translation_target)
                translation_dict_1.append({"en": translation_source, args.language: translation_target})
                true_markables_length.append(markable.count(" ") + 1)

    # add to output
    if len(translation_dict_1) > 0:
        fdict1.write(json.dumps(translation_dict_1, ensure_ascii=False) + "\n")
    else:
        fdict1.write("\n")
        
    # randomized dictionary
    translation_dict_2 = []
    markables_seen = set()


    possible_fixes = [(y,z) for x,y,z in data_fix2 if processed_sents+1 == x]
    if possible_fixes:
        # make sure the fixes appear there
        for markable_en, markable_cs in possible_fixes:
            assert markable_en in " ".join(sent_en) and markable_cs in " ".join(sent_cs)
            translation_dict_2.append({"en": markable_en, args.language: markable_cs})
    else:
        # generate automatically
        for markable_len in true_markables_length:
            attempts = 100
            while True:
                # reseed because we may be changing the history at places
                random.seed(" ".join(sent_cs + sent_en))
                markable_i = random.choice(range(len(sent_en)-markable_len+1))
                markable = " ".join(sent_en[markable_i:markable_i+markable_len])
                attempts -= 1
                if attempts == 0:
                    break
                # disallow true markables
                if markable.lower() in markables:
                    continue
                # remove several banned words
                if markable.lower() in {"the", "of"}:
                    continue
                translation_target, translation_source = align_markable(markable, sent_cs, sent_en)
                # translation_source, translation_target = mutate_markables(translation_source, translation_target, data_fix1)
                if (
                    len(translation_target) > 1 and
                    len(translation_target)/len(translation_source) > 0.3 and
                    len(translation_source)/len(translation_target) > 0.3 and
                    translation_source not in markables_seen and
                    translation_target not in markables_seen
                ):
                    markables_seen.add(translation_source)
                    markables_seen.add(translation_target)
                    translation_dict_2.append({"en": translation_source, args.language: translation_target})
                    break

    processed_sents += 1
    # add to output
    if len(translation_dict_2) > 0:
        fdict2.write(json.dumps(translation_dict_2, ensure_ascii=False) + "\n")
    else:
        fdict2.write("\n")