import sys
sys.path.append("../../alignments-pipelines/")
from alignment_pipelines import AlignmentMetrics 
from dataclasses import dataclass, asdict
import os


fastalign_alignment_metrics = AlignmentMetrics(
                                predicted_file="./outputs/fastalign_symmetric_alignments_train_en-pt.align",
                                reference_file="./references/train_gold_alignments.align", 
                              )
print(fastalign_alignment_metrics.evaluate())
