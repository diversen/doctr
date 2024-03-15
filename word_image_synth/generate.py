import json
import logging
import os
import random
import time
import uuid
import gc

from multiprocessing import Pool
from multiprocessing import Manager
from trdg.generators import GeneratorFromStrings
from doctr.datasets import VOCABS


import os
import json
import tempfile

def save_labels(data, target_file_path):

    data = dict(data)  # Convert to standard dict

    # Create a temporary file in the same directory as the target file
    dir_name = os.path.dirname(target_file_path)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, dir=dir_name) as tmp_file:
        json.dump(data, tmp_file, ensure_ascii=False, indent=4)
        temp_file_path = tmp_file.name

    # Atomically rename the temporary file to the target file
    os.rename(temp_file_path, target_file_path)


# find all .ttf files in /usr/share/fonts
def get_fonts():
    """
    Get all .ttf files in /usr/share/fonts
    """
    fonts = []
    for root, dirs, files in os.walk("/usr/share/fonts"):
        for file in files:
            if file.endswith(".ttf"):
                fonts.append(os.path.join(root, file))

    # Get all fonts except "DroidSansFallbackFull.ttf"
    # This does not support latin1
    fonts = [font for font in fonts if "DroidSansFallbackFull.ttf" not in font]

    # remove "/usr/share/fonts/truetype/msttcorefonts/webdings.ttf"
    # This does not support latin1

    fonts = [font for font in fonts if "webdings.ttf" not in font]

    # remove "Webdings.ttf"
    # This does not support latin1

    fonts = [font for font in fonts if "Webdings.ttf" not in font]

    return fonts


fonts = get_fonts()


text_colors = [
    "#000000",  # Black
    "#FF0000",  # Red
    "#00FF00",  # Green
    "#0000FF",  # Blue
    "#FFFF00",  # Yellow
    "#00FFFF",  # Cyan
    "#FF00FF",  # Magenta
    "#C0C0C0",  # Silver
    "#808080",  # Gray
    "#800000",  # Maroon
    "#808000",  # Olive
    "#008000",  # Dark Green
    "#800080",  # Purple
    "#008080",  # Teal
    "#000080",  # Navy
]


def generate_word(word, labels_dict, output_dir_images):
    """
    Generate an image for a single word
    """
    font = random.choice(fonts)
    text_color = random.choice(text_colors)
    distorsion_type = random.choice([0, 1, 2])
    size = random.randint(32, 124)  # Randomize font size
    skewing_angle = random.randint(0, 15)
    blur = random.choice([0, 1, 2])
    distorsion_orientation = random.choice([0, 1])
    space_width = random.uniform(0.5, 1.5)
    character_spacing = random.randint(0, 10)
    # Initialize the generator for the current word with configurations
    string_generator = GeneratorFromStrings(
        strings=[word],
        fonts=[font],
        language="da",
        size=size,
        skewing_angle=skewing_angle,
        random_skew=True,
        blur=blur,
        random_blur=True,
        distorsion_type=distorsion_type,
        distorsion_orientation=distorsion_orientation,
        alignment=1,
        text_color=text_color,
        # orientation=random.choice([0, 1]),
        background_type=random.choice([0, 1, 2]),
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


def generate_images_for_batch(words, output_dir_images, labels_dict, num_images_per_word):
    args = [(word, labels_dict, output_dir_images, num_images_per_word) for word in words]
    
    with Pool() as pool:
        pool.starmap(worker, args) 

def worker(word, labels_dict, output_dir_images, num_images_per_word):
    for _ in range(num_images_per_word):
        generate_word(word, labels_dict, output_dir_images)



def generate_images_from_words(words, begin_word, num_images_per_word, output_dir, batch_size=10):
    output_dir_images = os.path.join(output_dir, "images")
    os.makedirs(output_dir_images, exist_ok=True)
    labels_file = os.path.join(output_dir, "labels.json")

    if not os.path.exists(labels_file):
        with open(labels_file, "w", encoding="utf-8") as f:
            json.dump({}, f)

    manager = Manager()
    labels_dict = manager.dict()  # Create a managed dictionary

    
    with open(labels_file, "r") as f:
        initial_labels = json.load(f)
        labels_dict.update(initial_labels)

    processing_started = False if begin_word else True
    words_processed = 0

    # get start time
    start_time = time.time()

    for i, word in enumerate(words):
        if not processing_started:
            if word == begin_word:
                processing_started = True
            else:
                continue

        if (i % batch_size == 0 and i != 0) or (word == words[-1]):
            # Save after processing each batch or on the last word
            save_labels(labels_dict, labels_file)
            logging.info(f"Batch processed and saved. Total words processed: {words_processed}")

            # log time taken
            time_taken = time.time() - start_time

            # rounded time_taken per batch
            logging.info(f"Time taken per batch: {round(time_taken, 4)} seconds")

            # rounded time taken per word
            logging.info(f"Time taken per word: {round(time_taken / words_processed, 4)} seconds")

            # reset start time
            start_time = time.time()

        # Process the current word
        logging.info(f"Generating images for word: {word}")
        generate_images_for_batch([word], output_dir_images, labels_dict, num_images_per_word)
        words_processed += 1

    # Save any remaining changes after loop ends
    save_labels(labels_dict, labels_file)
    logging.info(f"Finished processing. Total words processed: {words_processed}")


def set_labels(labels_file, max_chars, max_labels=None, vocab=None, vocab_required=None):
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


def generate_subset_labels(labels_file, max_chars, max_labels, vocab):
    """
    Generate a subset of labels
    """
    with open(labels_file, "r", encoding="utf-8") as f:
        labels_dict = json.load(f)

    # size of labels before max chars
    logging.info(f"Size of labels before max labels: {len(labels_dict)}")

    vocab_chars = VOCABS[vocab]

    # remove labels that are not in vocab
    labels_dict = {key: value for key, value in labels_dict.items() if all(char in vocab_chars for char in value)}

    # remove labels that are greater than max_chars
    labels_dict = {key: value for key, value in labels_dict.items() if len(value) <= max_chars}

    # continue if value has chars that are not in vocab
    # if not all(char in vocab_chars for char in value):
    #     continue

    # randomize labels
    labels_keys = list(labels_dict.keys())
    random.shuffle(labels_keys)

    # Correctly utilizing shuffled labels_keys
    labels_subset = {}
    for key in labels_keys[:max_labels]:
        labels_subset[key] = labels_dict[key]

    labels_subset_file = labels_file.replace(".json", f"_subset_{max_labels}.json")
    with open(labels_subset_file, "w", encoding="utf-8") as f:
        json.dump(labels_subset, f, ensure_ascii=False, indent=4)

    # print size of labels
    logging.info(f"Size of labels: {len(labels_subset)}")

    logging.info(f"Saved {labels_subset_file}.")
    return labels_subset_file
