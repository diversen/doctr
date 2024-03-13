import json
import logging

from doctr.datasets import VOCABS
from word_image_synth.default_logger import configure_app_logging  # noqa: E402
from word_image_synth.generate import set_labels, generate_subset_labels

configure_app_logging()


set_labels("/home/dennis/d/train/labels.json", max_chars=32, vocab="danish")
set_labels("/home/dennis/d/validation/labels.json", max_chars=32, vocab="danish")

# generate_subset_labels("/home/dennis/d/train/labels.json", 20000)
# generate_subset_labels("/home/dennis/d/validation/labels.json", 5000)
