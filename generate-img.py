import argparse
import json
import logging
import asyncio

from doctr.datasets import VOCABS
from word_image_synth.default_logger import configure_app_logging  # noqa: E402
from word_image_synth.generate import generate_images_from_word
from word_image_synth.wiki import generate_word_list

configure_app_logging()

# get num_words from args --num-words
parser = argparse.ArgumentParser(description="Generate images from a list of words")
parser.add_argument(
    "--num-words", type=int, default=20, help="Minimum number of words to generate. It may generate more words."
)

# get output dir from args --output-dir
parser.add_argument(
    "--output-dir", type=str, default="/home/dennis/d", help="Output directory"
)

# word list
parser.add_argument("--word-list", type=str, default="words.json", help="Word list")

# begin word in case of resuming from a word
parser.add_argument(
    "--begin-word", type=str, default=None, help="Begin word in case of resuming"
)

# Add arguments specifying number of images to generate per word
parser.add_argument(
    "--num-images-per-word",
    type=int,
    default=20,
    help="Number of images to generate per word",
)

# Add argument for vocab
parser.add_argument(
    "--vocab",
    type=str,
    default="danish",
    help="Vocab to use for generating words",
)

# add argument for lang --lang, used in generate_word_list wiki
parser.add_argument(
    "--lang",
    type=str,
    default="da",
    help="Language to use for generating words",
)


# get all args
args = parser.parse_args()
num_words = args.num_words
output_dir = args.output_dir
word_list = args.word_list
begin_word = args.begin_word
num_images_per_word = args.num_images_per_word
vocab = args.vocab
lang = args.lang


# from word_image_synth.generate import random_num_words  # noqa: E402
asyncio.run(generate_word_list(word_list, num_words, vocab, lang=lang, concurrent_requests=5, save_every_n_tasks=10))

# read words from json file
with open(word_list, "r", encoding="utf-8") as f:
    words = json.load(f)

for word in words:

    if begin_word and word != begin_word:
        continue

    begin_word = None

    logging.debug(f"Generating images for {word}")
    generate_images_from_word(
        word=word, num_images=num_images_per_word, output_dir=output_dir,
    )
