#!/usr/bin/env python3

import json
import numpy as np
import mosestokenizer

for lang1, lang2 in [("de", "en"), ("en", "cs"), ("zh", "en")]:
    tokenizer1 = mosestokenizer.MosesTokenizer(lang=lang1)
    tokenizer2 = mosestokenizer.MosesTokenizer(lang=lang2)
    text_lang1 = [tokenizer1(x) for x in open(f"data_test/{lang1}{lang2}.{lang1}", "r")]
    text_lang2 = [tokenizer2(x) for x in open(f"data_test/{lang1}{lang2}.{lang2}", "r")]
    terms_proper = [json.loads(x) for x in open(f"data_test/{lang1}{lang2}.term.proper", "r")]
    terms_random = [json.loads(x) for x in open(f"data_test/{lang1}{lang2}.term.random", "r")]
    print(
        f"\\{lang1}{lang2}",
        len(text_lang1),
        f"{np.average([len(line) for line in text_lang1]):.1f}/"
        f"{np.average([len(line) for line in text_lang2]):.1f}",
        f"{np.average([len(line) for line in terms_proper]):.1f}/"
        f"{np.average([len(line) for line in terms_random]):.1f}",
        sep=" & ", end=r"\\"+"\n"
    )