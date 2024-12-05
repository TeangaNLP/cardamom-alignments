import sys
sys.path.append("../../alignments-pipelines/")
from alignment_pipelines import AlignmentMetrics 
from dataclasses import dataclass, asdict
import os
import collections


results = collections.defaultdict(dict)
for f in os.listdir("./outputs/"):
    if not ".pharaoh" in f:
        continue
    predicted_file=f"./outputs/{f}"
    #fast_align 
    lang  = f.split("_")[2] 
    split = f.split("_")[3].split(".")[0] 
    # lang, split  = f.split(".")[0].split("_")
    print(lang, split)
    gold_file=f"./references/{lang}_{split}.tsv.gold"
    fastalign_alignment_metrics = AlignmentMetrics(
                                    predicted_file=predicted_file,
                                    reference_file=gold_file, 
                                  )
    eval_ = fastalign_alignment_metrics.evaluate()
    results[lang][split] = eval_
    print(gold_file, eval_)
