import argparse
import asyncio
import json
import os
import random

from word_image_synth.default_logger import configure_app_logging
from word_image_synth.generate_images import generate_images_from_words
from word_image_synth.database import DatabaseManager


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate images from a list of words",
    )
    parser.add_argument(
        "--num-words",
        type=int,
        default=20,
        help="Minimum number of words to generate. It may generate more words.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Output directory",
    )

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
        "--begin-word",
        type=str,
        default=None,
        help="Begin word in case of resuming",
    )
    return parser.parse_args()


async def main():
    """The main function."""
    args = parse_args()

    print(args)

    num_words = args.num_words
    output_dir = args.output_dir
    num_images_per_word = args.num_images_per_word
    lang = args.lang

    db = DatabaseManager(output_dir)
    words = await db.get_words(lang, limit=num_words)

    generate_images_from_words(
        words=words,
        num_images_per_word=num_images_per_word,
        output_dir=output_dir,
        lang=lang,
    )

if __name__ == "__main__":
    configure_app_logging()
    asyncio.run(main())
