import json
import os
import logging

from doctr.datasets import VOCABS
from word_image_synth.default_logger import configure_app_logging  # noqa: E402
from word_image_synth.wiki import generate_num_words

configure_app_logging()

# from word_image_synth.generate import random_num_words  # noqa: E402
vocab = VOCABS["multilingual"]

generate_num_words("words.json", 50000, vocab)
# random_num_words("ÆØÅ TEST", 1000, "/home/dennis/d/images")
