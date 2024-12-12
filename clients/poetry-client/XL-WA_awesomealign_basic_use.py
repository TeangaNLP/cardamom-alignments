from alignment_pipelines import AwesomeAlignPipeline
from dataclasses import dataclass, asdict
from collections import defaultdict
import os

@dataclass
class AwesomeAlignConfig:
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
           output_fp = f"{self.__getattribute__('OUT_FOLDER')}{filename}"
           self.__setattr__('OUT_FP', output_fp)
        
if __name__ == "__main__":
    import itertools
    import os
    langs = ["bg","da","es","et","hu","it","nl","pt","ru","sl"]
    file_type = ["dev","train","test"]
    combinations = itertools.product(langs, file_type)
    for (lang, filetype_) in combinations: 
        config_dict = {
                "INP_FP": f"../../data/XL-WA/data/{lang}/{filetype_}.tsv", 
                "OUT_FOLDER": f'./outputs/XL-WA/data/{lang}/', 
                "MODEL": "bert",
                "TOKEN_TYPE": "bpe",
                "MATCHING_METHODS": "mai",
                }
        simAlignConfig = SimAlignConfig(**config_dict)
        os.system(f'mkdir -p {config_dict["OUT_FOLDER"]}')
        
        # making an instance of our model.
        # You can specify the embedding model and all alignment settings in the constructor.
        pipeline = SimAlignPipeline(config=simAlignConfig)
        models = defaultdict(
                lambda: {
                    "model_id": None,
                    "alignments":{},
                    }
                )

        # The source and target sentences should be tokenized to words.
        with open(simAlignConfig.INP_FP) as inpf:
            for line in inpf:
                print(line)
                src, trg, gold = line.split("\t")
                parallel_sent_pair_id = f"{src}-{trg}" 
                src_sentence_tokens = src.split(" ")
                trg_sentence_tokens = trg.split(" ")
                print(src_sentence_tokens, trg_sentence_tokens)
                alignments = pipeline(src_sentence_tokens, trg_sentence_tokens)
                
                print(alignments)
                for matching_method in alignments:
                    model_strategy_id = f"{simAlignConfig.MODEL}-{simAlignConfig.TOKEN_TYPE}-{matching_method}"
                    print(matching_method, ":", alignments[matching_method])
                    models[model_strategy_id]["model_id"] = model_strategy_id
                    models[model_strategy_id]["alignments"][parallel_sent_pair_id] = alignments[matching_method]
                print(models)
                print(gold)
            # The output is a dictionary with different matching methods.
            # Each method has a list of pairs indicating the indexes of aligned words (The alignments are zero-indexed).
            # Expected output:
            # mwmf (Match): [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
            # inter (ArgMax): [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
            # itermax (IterMax): [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
            for model_id, model_data in models.items():
                m = model_data
                model_output_fp = f'{simAlignConfig.OUT_FP}-{model_id}.tsv'
                with open(model_output_fp,"w") as outf:
                    for parallel_sent_pair_id, alignments_lst in m["alignments"].items():
                        alignments_str = " ".join([f"{sIdx}-{tIdx}" for sIdx, tIdx in alignments_lst]) 
                        tsv_row=f'{parallel_sent_pair_id}\t{alignments_str}\n'
                        outf.write(tsv_row)
