import argparse
import json
import logging

from doctr.datasets import VOCABS
from word_image_synth.default_logger import configure_app_logging  # noqa: E402
from word_image_synth.generate import generate_images_from_word
from word_image_synth.wiki import generate_word_list

configure_app_logging()

# get num_words from args --num-words
parser = argparse.ArgumentParser(description="Generate images from a list of words")
parser.add_argument(
    "--num-words", type=int, default=20, help="Number of words to generate"
)

# get output dir from args --output-dir
parser.add_argument(
    "--output-dir", type=str, default="/home/dennis/d", help="Output directory"
)

# word list
parser.add_argument("--word-list", type=str, default="words.json", help="Word list")

# get all args
args = parser.parse_args()
num_words = args.num_words
output_dir = args.output_dir
word_list = args.word_list

# from word_image_synth.generate import random_num_words  # noqa: E402
vocab = VOCABS["multilingual"]

generate_word_list(word_list, num_words, vocab)

# read words from json file
with open(word_list, "r", encoding="utf-8") as f:
    words = json.load(f)

for word in words:
    logging.debug(f"Generating images for {word}")
    generate_images_from_word(word, 20, output_dir)
