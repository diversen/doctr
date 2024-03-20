from word_image_synth.database import DatabaseManager
import argparse
import os
import json


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Export generated images to a dataset",
    )
    parser.add_argument(
        "--num-words",
        type=int,
        default=None,
        help="Minimum number of words to generate. It may generate more words.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Output directory",
    )
    parser.add_argument(
        "--lang",
        type=str,
        help="Language to use for generating words",
        default=None,
    )

    return parser.parse_args()

args = parse_args()
print(args)

db = DatabaseManager(args.output_dir)

labels = db.get_labels(lang=args.lang, limit=args.num_words)

# save labels as json file named labels.json encoded as utf-8 to the output directory
labels_json_path = os.path.join(args.output_dir, "labels.json")
with open(labels_json_path, "w", encoding="utf-8") as f:
    json.dump(labels, f, ensure_ascii=False, indent=4)

# Close the database connection
db.close()