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
    def __init__(self, model=None, token_type=None, matching_methods=None, **kwargs):
        # Check if config object is provided
        config = kwargs.get("config", None)
        
        # If config is provided, use its attributes; otherwise, use provided parameters
        if config:
            # Attribute access with default fallbacks
            self.model = getattr(config, "MODEL", model)
            self.token_type = getattr(config, "TOKEN_TYPE", token_type)
            self.matching_methods = getattr(config, "MATCHING_METHODS", matching_methods)
        else:
            # Use the directly provided parameters
            self.model = model
            self.token_type = token_type
            self.matching_methods = matching_methods

        # Ensure all required parameters are set, with default handling if needed
        if not self.model:
            raise ValueError("A 'model' parameter must be provided, either directly or via SimAlignConfig.")
        if not self.token_type:
            raise ValueError("A 'token_type' parameter must be provided, either directly or via SimAlignConfig.")
        if not self.matching_methods:
            raise ValueError("A 'matching_methods' parameter must be provided, either directly or via SimAlignConfig.")

        self.aligner = SentenceAligner(model=self.model, token_type=self.token_type, matching_methods=self.matching_methods)

    def __call__(self, src_sentence_tokens, trg_sentence_tokens):
        return self.run(src_sentence_tokens, trg_sentence_tokens)

    def run(self, src_sentence_tokens, trg_sentence_tokens):
        alignments = self.aligner.get_word_aligns(src_sentence_tokens, trg_sentence_tokens)
        print(src_sentence_tokens, trg_sentence_tokens)
        for matching_method in alignments:
            print('from inside',matching_method, ":", alignments[matching_method])
        return alignments

if __name__ == '__main__':
   pipeline = SimAlignPipeline();
   pipeline.run('../data/en-es.pharaoh')
