# WMT 2023 Terminology Shared Task Data

The current version contains both the sources, references, terminologies but also participant submissions.
It is easily accessible [from huggingface](https://huggingface.co/datasets/zouharvi/wmt-terminology-2023) and contains only the `test` split:

```python3
from datasets import load_dataset
data = load_dataset("zouharvi/wmt-terminology-2023")["test"]
print(len(data))
```

If you use this data, please [read the paper](https://aclanthology.org/2023.wmt-1.54/) and cite:

```
@inproceedings{semenov-etal-2023-findings,
    title = "Findings of the WMT 2023 Shared Task on Machine Translation with Terminologies",
    author = "Kirill Semenov and
              Vilém Zouhar and
              Tom Kocmi and
              Dongdong Zhang and
              Wangchunshu Zhou and
              Yuchen Eleanor Jiang"
    booktitle = "Proceedings of the Eight Conference on Machine Translation (WMT)",
    month = dec,
    year = "2023",
    publisher = "Association for Computational Linguistics",
}
```

The three language pairs for the test dataset are sourced from:
- [Czech and English abstracts of ÚFAL papers](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-4922) by Rudolf Rosa and Vilém Zouhar
- [MuchMore Springer Bilingual Corpus](https://muchmore.dfki.de/resources1.htm)
- [BWB Corpus](https://aclanthology.org/2023.acl-long.435/) by Yuchen Eleanor Jiang et al.

This project is a collaboration between ETH Zurich, AIWaves, Microsoft and Charles Univeristy.


## Previous version

Note: this method is deprecated.

Run the following to unpack the dev and test data (names differ from original task split):
```bash
git clone https://github.com/wmt-terminology-task/data-2023.git wmt-terminology-2023-data
cd wmt-terminology-2023-data
tar -xf data_dev/data.tar.gz -C data_dev
tar -xf data_test/data.tar.gz -C data_test
```

We strongly recommend not using the dev data beyond rundimentary sanity checks.
The dev set is very small and of lower quality; instead, please use the test split.
The test with references and terminologies are in `data_test/`:
```
deen.de
deen.en
deen.term.proper
deen.term.random
encs.cs
encs.en
encs.term.proper
encs.term.random
zhen.zh
zhen.en
zhen.term.proper
zhen.term.random
```

In 2023 we distinguished between "proper terminology" and "random (but correctly translated) terminology".
In all cases, the terminology source and target appear in the source and target sentences. 

```bash
awk "FNR==33{print;nextfile}" data_test/deen.{en,de,term.proper,term.random}

> Most informative is the analysis of airway secretions:
> Häufig jedoch führt die Analyse von Material aus den Atemwegen zur Diagnose:
> [{"en": "analysis of airway secretions", "de": "Analyse von Material aus den Atemwegen"}]
> [{"en": "Most", "de": "Häufig"}]
```

The scripts in this repository are purely for reproduction purposes and in normal situations should not be used.

