import argparse
import json
import logging
import asyncio
import os

from doctr.datasets import VOCABS
from word_image_synth.default_logger import configure_app_logging
from word_image_synth.generate import generate_images_from_words  # Renamed function
from word_image_synth.wiki import generate_word_list

configure_app_logging()

def parse_args():
    parser = argparse.ArgumentParser(description="Generate images from a list of words")
    parser.add_argument(
        "--num-words", type=int, default=20, help="Minimum number of words to generate. It may generate more words."
    )
    parser.add_argument(
        "--output-dir", type=str, default="/home/dennis/d", help="Output directory"
    )
    parser.add_argument("--word-list", type=str, default="words.json", help="Word list")

    parser.add_argument(
        "--num-images-per-word",
        type=int,
        default=20,
        help="Number of images to generate per word",
    )
    parser.add_argument(
        "--vocab",
        type=str,
        default="danish",
        help="Vocab to use for generating words",
    )
    parser.add_argument(
        "--lang",
        type=str,
        default="da",
        help="Language to use for generating words",
    )

    parser.add_argument(
        "--begin-word", type=str, default=None, help="Begin word in case of resuming"
    )
    return parser.parse_args()

async def main():
    args = parse_args()
    num_words = args.num_words
    output_dir = args.output_dir
    begin_word = args.begin_word
    num_images_per_word = args.num_images_per_word
    vocab = args.vocab
    lang = args.lang

    word_list_path = os.path.join(output_dir, 'words.json')

    # Generate output_dir if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate words.json file if it does not exist
    if not os.path.exists(word_list_path):
        with open(word_list_path, "w", encoding="utf-8") as f:
            json.dump([], f)

    await generate_word_list(word_list_path, num_words, vocab, lang=lang, concurrent_requests=10, save_every_n_tasks=10)

    with open(word_list_path, "r", encoding="utf-8") as f:
        words = json.load(f)

    generate_images_from_words(
        words=words,
        begin_word=begin_word,
        num_images_per_word=num_images_per_word,
        output_dir=output_dir,
        batch_size=100  # New parameter to define how many words are processed before saving the JSON file
    )

if __name__ == "__main__":
    asyncio.run(main())
