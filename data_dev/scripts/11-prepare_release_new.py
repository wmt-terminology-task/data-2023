#!/usr/bin/env python3

import sacremoses

# tar -czf data_dev/data.tar.gz -C data_dev/raw4/ .


for lang1, lang2 in [
    ("en", "cs"),
    ("de", "en"),
    ("zh", "en"),
]:
    lang1r = lang1 if lang2 != "cs" else lang2
    lang2r = lang2 if lang2 != "cs" else lang1

    is_zh = lang1 == "zh"

    
    def dump_file(suffix, data):
        if is_zh and suffix == "en":
            detokenizer = sacremoses.MosesDetokenizer(lang="en")
            data = [detokenizer.detokenize([line]) for line in data]
        with open(f"data_dev/raw4/{lang1}{lang2}.{suffix}", "w") as f:
            f.write("\n".join(data))
            
    data_raw_l1 = [
        line.rstrip("\n")
        for line in open(f"data_dev/raw3/dev.{lang1r}-{lang2r}.{lang1}", "r")
    ]+[
        line.rstrip("\n")
        for line in open(f"data_dev/raw3/test.{lang1r}-{lang2r}.{lang1}", "r")
    ]
    data_raw_l2 = [
        line.rstrip("\n")
        for line in open(f"data_dev/raw3/dev.{lang1r}-{lang2r}.{lang2}", "r")
    ]+[
        line.rstrip("\n")
        for line in open(f"data_dev/raw3/test.{lang1r}-{lang2r}.{lang2}", "r")
    ]
    data_raw_term = [
        line.rstrip("\n")
        for line in open(f"data_dev/raw3/dev.{lang1r}-{lang2r}.dict.jsonl", "r")
    ]+[
        line.rstrip("\n")
        for line in open(f"data_dev/raw3/test.{lang1r}-{lang2r}.dict.jsonl", "r")
    ]
    dump_file(
        lang1,
        [
            line for line_i, line in enumerate(data_raw_l1)
            if line_i % 3 == 0
        ],
    )

    dump_file(
        lang2,
        [
            line for line_i, line in enumerate(data_raw_l2)
            if line_i % 3 == 0
        ],
    )

    dump_file(
        "term.proper",
        [
            line if line else "[]"
            for line_i, line in enumerate(data_raw_term) if line_i % 3 == 1
        ],
    )
    dump_file(
        "term.random",
        [
            line if line else "[]"
            for line_i, line in enumerate(data_raw_term) if line_i % 3 == 2
        ],
    )

