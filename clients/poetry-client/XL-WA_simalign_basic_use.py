from alignment_pipelines import SimAlignPipeline
from dataclasses import dataclass, asdict
import os

@dataclass
class SimAlignConfig:
    INP_FP: str = None
    OUT_FOLDER: str = None
    OUT_FP: str = None
    MODEL: str = None
    TOKEN_TYPE: str = None
    MATCHING_METHODS: str = None

    #def __post_init__(self):
    #   for field in self.__dataclass_fields__:
    #       print(self.__getattribute__(field))

    def __post_init__(self):
        # Independent check: Ensure certain fields are not None
        independent_fields = ['INP_FP', 'MODEL', 'TOKEN_TYPE', 'MATCHING_METHODS']
        for field in independent_fields:
            if self.__getattribute__(field) is None:
                raise ValueError(f"{field} should not be None")

        # Either-or check: Ensure exactly one of each pair is set
        either_or_pairs = [('OUT_FOLDER', 'OUT_FP')]
        for field1, field2 in either_or_pairs:
            value1 = self.__getattribute__(field1)
            value2 = self.__getattribute__(field2)
            if (value1 is None) == (value2 is None):  # Both are None or both are defined
                raise ValueError(f"Exactly one of {field1} or {field2} must be set, not both or neither")

        if self.__getattribute__('OUT_FP') is None:
           filename = self.__getattribute__('INP_FP').split(os.sep)[-1] # assumes filenames will not end with "/"(os.sep)
           output_fp = f"{self.__getattribute__('OUT_FOLDER')}/{filename}"
           self.__setattr__('OUT_FP', output_fp)
        
config_dict = {
        "INP_FP": '../../data/XL-WA/data/pt/test.tsv', 
        "OUT_FOLDER": './outputs/XL-WA/data/pt/test.tsv', 
        "MODEL": "bert",
        "TOKEN_TYPE": "bpe",
        "MATCHING_METHODS": "mai",
        }
simAlignConfig = SimAlignConfig(**config_dict)

# making an instance of our model.
# You can specify the embedding model and all alignment settings in the constructor.
pipeline = SimAlignPipeline(**asdict(simAlignConfig))

# The source and target sentences should be tokenized to words.
with open(simAlignConfig.INP_FP) as inpf:
    for line in inpf:
        print(line)
        src, trg, gold = line.split("\t")
        src_sentence_tokens = src.split(" ")
        trg_sentence_tokens = trg.split(" ")
        print(src_sentence_tokens, trg_sentence_tokens)
        alignments = pipeline(src_sentence_tokens, trg_sentence_tokens)

        for matching_method in alignments:
            print(matching_method, ":", alignments[matching_method])
        print(gold)
        input()
    # The output is a dictionary with different matching methods.
    # Each method has a list of pairs indicating the indexes of aligned words (The alignments are zero-indexed).
# Expected output:
# mwmf (Match): [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
# inter (ArgMax): [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
# itermax (IterMax): [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
