from simalign import SentenceAligner
import sys
from collections import defaultdict

# making an instance of our model.
# You can specify the embedding model and all alignment settings in the constructor.
model="bert"
token_type="bpe"
matching_methods="mai"
myaligner = SentenceAligner(model=model, token_type=token_type, matching_methods=matching_methods)

# The source and target sentences should be tokenized to words.
default_fo='../../data/XL-WA/data/pt/test.tsv'
dataset_fp= sys.argv[1] if len(sys.argv) > 1 else default_fp 
models = defaultdict(lambda: defaultdict(dict))
with open(dataset_fp) as inpf:
    for line in inpf:
        src, trg, gold = line.split("\t")
        src_sentence = src.split(" ")
        sent_id = f"{src}_{trg}"
        trg_sentence = trg.split(" ")
        print(src_sentence, trg_sentence)
        alignments = myaligner.get_word_aligns(src_sentence, trg_sentence)

        for matching_method in alignments:
            model_id = f"model_{model}_{token_type}_{matching_method}"
            models[sent_id][model_id]["alignments"] =  alignments[matching_method]
            models[sent_id][model_id]["id"] = model_id
        print(models)
        input()
    # The output is a dictionary with different matching methods.
    # Each method has a list of pairs indicating the indexes of aligned words (The alignments are zero-indexed).
# Expected output:
# mwmf (Match): [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
# inter (ArgMax): [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
# itermax (IterMax): [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
