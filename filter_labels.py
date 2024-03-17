import json
import logging

from doctr.datasets import VOCABS
from word_image_synth.default_logger import configure_app_logging  # noqa: E402
from word_image_synth.generate import set_labels, generate_subset_labels

configure_app_logging()


# set_labels("/home/dennis/d/train/labels.json.backup", max_chars=32, max_labels=50000, vocab="danish", vocab_required="éæøåÉÆØÅ")
# set_labels("/home/dennis/d/validation/labels.json.backup", max_chars=32, max_labels=10000, vocab="danish", vocab_required="éæøåÉÆØÅ")

generate_subset_labels(
    "train-data/labels.json",
    max_chars=32,
    max_labels=1000000,
    vocab="danish",
)
generate_subset_labels(
    "validation-data/labels.json",
    max_chars=32,
    max_labels=1000000,
    vocab="danish",
)
