import logging
import os
import uuid
from multiprocessing import Manager, Pool
import settings
from word_image_synth.database import DatabaseManager
from trdg.generators import GeneratorFromStrings


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
    """ "Worker function to generate images for a single word."""
    for _ in range(num_images_per_word):
        word_cased = settings.transform_word(word)
        generate_word(word_cased, labels_dict, output_dir_images)


def generate_images_from_words(
    words,
    num_images_per_word,
    output_dir,
    lang,
):
    db = DatabaseManager(output_dir)
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
        db.save_labels_to_db(labels_dict, lang)
        words_processed += 1

    logging.info(f"Finished processing. Total words processed: {words_processed}")
