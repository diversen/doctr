import argparse
import asyncio
import os

from word_image_synth.default_logger import configure_app_logging
from word_image_synth.wiki import generate_word_list


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

    return parser.parse_args()


async def main():
    """The main function."""
    args = parse_args()
    num_words = args.num_words
    output_dir = args.output_dir
    vocab = args.vocab
    lang = args.lang

    print(args)

    # Generate output_dir if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    await generate_word_list(
        output_dir,
        num_words,
        vocab,
        lang=lang,
        concurrent_requests=4,
    )


if __name__ == "__main__":
    configure_app_logging()
    asyncio.run(main())
