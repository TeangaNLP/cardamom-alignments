# -*- coding: utf-8 -*-
"""Example Google style docstrings.
    implements all steps required from
    loading parallel sentences files
    to output alignments

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
from simalign import SentenceAligner

class SimAlignPipeline:
    '''
        Given SimAlign configs
        setup the aligner
        preprocess the parallel sentences
        outputting alignments for each parallel pair
    '''
    def __init__(self):
        self.aligner = SentenceAligner(model="bert", token_type="bpe", matching_methods="mai")


    def run(self, sentences_fp):
        # making an instance of our model.
        # You can specify the embedding model and all alignment settings in the constructor.

        # The source and target sentences should be tokenized to words.
        with open(sentences_fp) as inpf:
            for line in inpf:
                line = line.strip()
                src_sentence, trg_sentence = line.split('|||')

                # The output is a dictionary with different matching methods.
                # Each method has a list of pairs indicating the indexes of aligned words (The alignments are zero-indexed).
                alignments = self.aligner.get_word_aligns(src_sentence, trg_sentence)

                print(src_sentence, trg_sentence)
                for matching_method in alignments:
                    print(matching_method, ":", alignments[matching_method])
                input()
                # Expected output:
                # mwmf (Match): [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
                # inter (ArgMax): [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
                # itermax (IterMax): [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)] 



if __name__ == '__main__':
   pipeline = SimAlignPipeline();
   pipeline.run('../data/en-es.pharaoh')
