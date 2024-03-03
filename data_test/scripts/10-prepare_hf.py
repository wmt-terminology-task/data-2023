import glob
import collections
import csv
import json

data_out = collections.defaultdict(lambda: {"src": None, "ref": None, "systems": collections.defaultdict(dict), "hints": {"rand": None, "term": None}})

for file in glob.glob("tmp/split_submissions/*.blind.*"):
    fname = file.split("/")[-1]

    is_zhen = ".zh-en." in fname
    is_deen = ".de-en." in fname
    is_encs = ".en-cs." in fname
    if is_zhen:
        langs_name = "zh-en"
    elif is_deen:
        langs_name = "de-en"
    elif is_encs:
        langs_name = "en-cs"
    else:
        raise Exception()

    is_base = fname.startswith("base.")
    is_rand = fname.startswith("rand.")
    is_term = fname.startswith("term.")
    if is_base:
        hints_name = "base"
    elif is_rand:
        hints_name = "rand"
    elif is_term:
        hints_name = "term"
    else:
        raise Exception()
    
    sys_name = fname.removeprefix(hints_name + ".").removesuffix(f".blind.{langs_name}.tsv")

    for line in csv.DictReader(open(file, "r"), delimiter="\t"):
        line_out = data_out[(line["src"], line["ref"])]
        line_out["src"] = line["src"]
        line_out["ref"] = line["ref"]
        line_out["langs"] = langs_name
        line_out["systems"][sys_name][hints_name] = line["mt"]
        if not is_base:
            line_out["hints"][hints_name] = json.loads(line["terms"])

data_out = list(data_out.values())

with open("test.json", "w") as f:
    json.dump(data_out, f, ensure_ascii=False, indent=2)