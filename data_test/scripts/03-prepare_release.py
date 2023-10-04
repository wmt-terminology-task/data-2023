#!/usr/bin/env python3

import sacremoses
import os

os.makedirs("data_test/raw2", exist_ok=True)

# tar -czf data_test/data.tar.gz -C data_test/raw2/ .

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
        with open(f"data_test/raw2/{lang1}{lang2}.{suffix}", "w") as f:
            f.write("\n".join(data))
            
    data_raw = [
        line.rstrip("\n")
        for line in open(f"data_test/raw/Final_terminology_{lang1}_{lang2}.txt", "r")
    ]
    dump_file(
        lang1,
        [
            line for line_i, line in enumerate(data_raw)
            if (not is_zh and line_i % 5 == 1) or (is_zh and line_i % 5 == 0)
        ],
    )

    dump_file(
        lang2,
        [
            line for line_i, line in enumerate(data_raw)
            if (not is_zh and line_i % 5 == 0) or (is_zh and line_i % 5 == 1)
        ],
    )

    dump_file(
        "term.proper" if not is_zh else "term.random",
        [
            line if line else "[]"
            for line_i, line in enumerate(data_raw) if line_i % 5 == 2
        ],
    )
    dump_file(
        "term.random" if not is_zh else "term.proper",
        [
            line if line else "[]"
            for line_i, line in enumerate(data_raw) if line_i % 5 == 3
        ],
    )

