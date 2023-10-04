#!/usr/bin/env python3

import sacremoses
import os

os.makedirs("data_dev/raw2", exist_ok=True)

# tar -czf data_dev/data.tar.gz -C data_dev/raw2/ .


for lang1, lang2 in [
    ("en", "cs"),
    ("de", "en"),
    ("zh", "en"),
]:
    is_zh = lang1 == "zh"
    
    def dump_file(suffix, data):
        if is_zh and suffix == "en":
            detokenizer = sacremoses.MosesDetokenizer(lang="en")
            data = [detokenizer.detokenize([line]) for line in data]
        with open(f"data_dev/raw2/{lang1}{lang2}.{suffix}", "w") as f:
            f.write("\n".join(data))
            
    data_raw_l1 = [
        line.rstrip("\n")
        for line in open(f"data_dev/raw/dev.{lang1}-{lang2}.{lang1}", "r")
    ]
    data_raw_l2 = [
        line.rstrip("\n")
        for line in open(f"data_dev/raw/dev.{lang1}-{lang2}.{lang2}", "r")
    ]
    data_raw_term = [
        line.rstrip("\n")
        for line in open(f"data_dev/raw/dev.{lang1}-{lang2}.dict.jsonl", "r")
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

