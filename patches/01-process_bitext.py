#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import json
import argparse
import random
random.seed(0)

args = argparse.ArgumentParser()
args = args.parse_args()

def process_align_line(align_txt):
    align_txt = [[int(y) for y in x.split("-")] for x in align_txt.split(" ")]
    return align_txt

root_en = ET.parse('data/raw/de-en.en.xml').getroot()
root_de = ET.parse('data/raw/de-en.de.xml').getroot()
data_align = open("data/raw/de-en.all.align", "r").read().rstrip().split("\n")

markables = set(open("data/raw/de-en.markables.en", "r").read().rstrip().split("\n"))
markables = {x.lower() for x in markables}

root_bitext = ET.parse('data/raw/de-en.bitext.xml').getroot()
links = list(root_bitext.findall("linkGrp")[0].findall("link"))

fen = open("data/clean/de-en.en", "w")
fde = open("data/clean/de-en.de", "w")
fdict1 = open("data/clean/de-en.dict1.jsonl", "w")
fdict2 = open("data/clean/de-en.dict2.jsonl", "w")

for align_i, align_link in enumerate(links):
    sent_from, sent_to = align_link.attrib["xtargets"].split(";")

    # remove possibly problematic alignments
    if len(sent_from.split(" ")) > 1 or len(sent_to.split(" ")) > 1 or sent_from != sent_to:
        continue

    # disregard the first \n token
    sent_en = [w.text for w in root_en.findall(f'.s[@id="{sent_from}"]')[0].iter()][1:]
    sent_de = [w.text for w in root_de.findall(f'.s[@id="{sent_to}"]')[0].iter()][1:]
    align = process_align_line(data_align[align_i])

    if len(sent_en)/len(sent_de) < 0.5 or len(sent_en)/len(sent_de) > 2:
        continue

    # x[0] is German, x[1] is English
    assert max([x[1] for x in align]) < len(sent_en) and max([x[0] for x in align]) < len(sent_de)

    fen.write(" ".join(sent_en)+"\n")
    fde.write(" ".join(sent_de)+"\n")

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
            translation_target += [sent_de[x] for x in alignment_targets_i]
            
        translation_target = " ".join(translation_target)
        translation_source = sent_trunk[:len(markable)]
        if len(translation_target) > 1 and len(translation_target)/len(translation_source) > 0.5 and len(translation_target)/len(translation_source) < 2:
            translation_dict_2.append({"en": translation_source, "de": translation_target})

    if len(translation_dict_2) > 0:
        fdict2.write(json.dumps(translation_dict_2, ensure_ascii=False) + "\n")
    else:
        fdict2.write("\n")

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
                translation_target += [sent_de[x] for x in alignment_targets_i]
                
            translation_target = " ".join(translation_target)
            translation_source = sent_trunk[:len(markable)]
            if len(translation_target) > 1 and len(translation_target)/len(translation_source) > 0.5 and len(translation_target)/len(translation_source) < 2:
                translation_dict_1.append({"en": translation_source, "de": translation_target})

    if len(translation_dict_1) > 0:
        fdict1.write(json.dumps(translation_dict_1, ensure_ascii=False) + "\n")
    else:
        fdict1.write("\n")