import json
import logging
import os
import random
import sqlite3
import time
import uuid
from multiprocessing import Manager, Pool

from trdg.generators import GeneratorFromStrings

# import all from settings under the namespace `settings`
import settings
from doctr.datasets import VOCABS


def init_db(output_dir_images):
    """
    Initialize the SQLite database and create the labels table if it doesn't exist.
    """
    db_path = os.path.join(output_dir_images, "database.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS labels (
            image_name TEXT PRIMARY KEY,
            word TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


def save_labels_to_db(labels_dict, output_dir_images):
    """
    Save labels to the SQLite database.
    """
    init_db(output_dir_images)

    db_path = os.path.join(output_dir_images, "database.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for image_name, word in labels_dict.items():
        c.execute(
            """
            INSERT INTO labels (image_name, word) VALUES (?, ?)
            ON CONFLICT(image_name) DO UPDATE SET word=excluded.word;
        """,
            (image_name, word),
        )
    conn.commit()
    conn.close()


def generate_word(word, labels_dict, output_dir_images):
    """
    Generate an image for a single word
    """
    font = settings.get_font()
    text_color = settings.get_text_color()
    distorsion_type = settings.distorsion_type

    size = settings.get_size()
    space_width = settings.get_space_width()
    character_spacing = settings.get_character_spacing()

    skewing_angle = settings.get_skewing_angle()
    blur = settings.get_blur()
    distorsion_orientation = settings.get_distorsion_orientation()
    background_type = settings.get_background_type()
    space_width = settings.get_space_width()
    character_spacing = settings.get_character_spacing()

    # language = settings.language
    orientation = settings.orientation

    # Initialize the generator for the current word with configurations
    string_generator = GeneratorFromStrings(
        strings=[word],
        fonts=[font],
        # language=language,
        size=size,
        skewing_angle=skewing_angle,
        random_skew=True,
        blur=blur,
        random_blur=True,
        distorsion_type=distorsion_type,
        distorsion_orientation=distorsion_orientation,
        alignment=1,
        text_color=text_color,
        stroke_fill=text_color,
        orientation=orientation,
        background_type=background_type,
        space_width=space_width,
        character_spacing=character_spacing,
        margins=(5, 5, 5, 5),
        fit=True,
    )

    # Generate a single image for the current word and then break the loop
    for img, lbl in string_generator:

        # Generate random string for the image name
        uuid_str = uuid.uuid4()

        image_name = f"{uuid_str}.png"
        img_path = os.path.join(output_dir_images, image_name)
        img.save(img_path)

        labels_dict[image_name] = word
        break


def generate_images_for_batch(
    words,
    output_dir_images,
    labels_dict,
    num_images_per_word,
):
    """Generate images for a batch of words."""
    args = [
        (
            word,
            labels_dict,
            output_dir_images,
            num_images_per_word,
        )
        for word in words
    ]

    with Pool() as pool:
        pool.starmap(worker, args)


def worker(
    word,
    labels_dict,
    output_dir_images,
    num_images_per_word,
):
    """"Worker function to generate images for a single word."""
    for _ in range(num_images_per_word):
        word_cased = settings.transform_word(word)
        generate_word(word_cased, labels_dict, output_dir_images)


def generate_images_from_words(
    words,
    begin_word,
    num_images_per_word,
    output_dir,
):
    """
    Generate images for a list of words.
    """
    output_dir_images = os.path.join(output_dir, "images")
    os.makedirs(output_dir_images, exist_ok=True)

    manager = Manager()
    words_processed = 0

    for i, word in enumerate(words):

        labels_dict = manager.dict()
        logging.info(
            f"{i + 1}/{len(words)}. Generating {num_images_per_word} images for word: {word}"
        )

        generate_images_for_batch(
            [word], output_dir_images, labels_dict, num_images_per_word
        )
        save_labels_to_db(labels_dict, output_dir)
        words_processed += 1

    logging.info(f"Finished processing. Total words processed: {words_processed}")


def set_labels(
    labels_file,
    max_chars,
    max_labels=None,
    vocab=None,
    vocab_required=None,
):
    """
    Generate labels for a max number of chars
    """
    with open(labels_file, "r", encoding="utf-8") as f:
        labels_dict = json.load(f)

    # size of labels before max chars
    logging.info(f"Size of labels before max chars: {len(labels_dict)}")

    filtered_labels = {}
    for key, value in labels_dict.items():

        if vocab:
            vocab_chars = VOCABS[vocab]

            # continue if value has chars that are not in vocab
            if not all(char in vocab_chars for char in value):
                continue

            if vocab_required:

                # if there is not a single char in value that is in vocab_chars then continue
                if not any(char in vocab_required for char in value):
                    continue

        if len(value) <= max_chars:
            filtered_labels[key] = value

    if max_labels:
        # random select max_labels from labels_max_chars
        filtered_labels = dict(random.sample(filtered_labels.items(), max_labels))

    # get path from labels_file
    labels_path = os.path.dirname(labels_file)

    # labels_max_chars_file = labels_file.replace(".json", f"_filtered.json.backup")
    labels_filtered_file = labels_path + "/labels_filtered.json"
    with open(labels_filtered_file, "w", encoding="utf-8") as f:
        json.dump(filtered_labels, f, ensure_ascii=False, indent=4)

    # print size of labels
    logging.info(f"Size of labels: {len(filtered_labels)}")
    logging.info(f"Saved {labels_filtered_file}.")


def generate_subset_labels(
    labels_file,
    max_chars,
    max_labels,
    vocab,
):
    """
    Generate a subset of labels
    """
    with open(labels_file, "r", encoding="utf-8") as f:
        labels_dict = json.load(f)

    # add backup of labels_file
    labels_backup_file = labels_file.replace(".json", f".json.backup")

    os.system(f"cp {labels_file} {labels_backup_file}")

    # size of labels before max chars
    logging.info(f"Size of labels before max labels: {len(labels_dict)}")

    vocab_chars = VOCABS[vocab]

    # remove labels that are not in vocab
    labels_dict = {
        key: value
        for key, value in labels_dict.items()
        if all(char in vocab_chars for char in value)
    }

    # remove labels that are greater than max_chars
    labels_dict = {
        key: value for key, value in labels_dict.items() if len(value) <= max_chars
    }

    # randomize labels
    labels_keys = list(labels_dict.keys())
    random.shuffle(labels_keys)

    # Correctly utilizing shuffled labels_keys
    labels_subset = {}
    for key in labels_keys[:max_labels]:
        labels_subset[key] = labels_dict[key]

    with open(labels_file, "w", encoding="utf-8") as f:
        json.dump(labels_subset, f, ensure_ascii=False, indent=4)

    # print size of labels
    logging.info(f"Size of labels: {len(labels_subset)}")
    logging.info(f"Saved {labels_file}.")
