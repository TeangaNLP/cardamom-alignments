from alignments_pipeline import SimAlignPipeline

# making an instance of our model.
# You can specify the embedding model and all alignment settings in the constructor.
pipeline = SimAlignPipeline(model="bert", token_type="bpe", matching_methods="mai")

# The source and target sentences should be tokenized to words.
with open('./data/pt/test.tsv') as inpf:
    for line in inpf:
        src, trg, gold = line.split("\t")
        src_sentence = src.split(" ")
        trg_sentence = trg.split(" ")
        print(src_sentence, trg_sentence)
        alignments = pipeline.run(src_sentence, trg_sentence)

        for matching_method in alignments:
            print(matching_method, ":", alignments[matching_method])
        input()
    # The output is a dictionary with different matching methods.
    # Each method has a list of pairs indicating the indexes of aligned words (The alignments are zero-indexed).
# Expected output:
# mwmf (Match): [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
# inter (ArgMax): [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
# itermax (IterMax): [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
