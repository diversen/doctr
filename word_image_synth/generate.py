import json
import logging
import os
import random
import time
import uuid

from trdg.generators import GeneratorFromStrings


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


def generate_images_from_word(word, num_words, output_dir="images_output"):
    """
    Generate images for a single word
    """
    logging.info(f"Generating {num_words} images for {word}.")
    output_dir_images = os.path.join(output_dir, "images")
    os.makedirs(output_dir_images, exist_ok=True)
    labels_file = os.path.join(output_dir, "labels.json")

    if os.path.exists(labels_file):
        with open(labels_file, "r", encoding="utf-8") as f:
            labels_dict = json.load(f)
            logging.info(f"Loaded {labels_file}")
    else:
        labels_dict = {}

    start = time.time()
    for _ in range(num_words):
        generate_word(word, labels_dict, output_dir_images)

    # save labels_dict to labels_file
    with open(labels_file, "w", encoding="utf-8") as f:
        json.dump(labels_dict, f, ensure_ascii=False, indent=4)

    end = time.time()
    logging.info(f"Saved {labels_file}. Generated {num_words} images for {word}.")
    logging.info(f"Time taken: {end - start:.2f} seconds.")
