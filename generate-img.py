import os
import random
from PIL import Image
from doctr.datasets import VOCABS
from trdg.generators import GeneratorFromStrings
import uuid
import json


print("VOCABS", VOCABS["danish"])
# 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~°£€¥¢฿æøåÆØÅ

# Common font paths on Linux systems (adjust according to your system)
fonts = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",  # Monospaced variant
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",  # Assuming Ubuntu Mono Regular
]

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

# Path to the Danish words file
words_file_path = "venv/lib/python3.10/site-packages/trdg/dicts/da.txt"

# Read all Danish words from the file
with open(words_file_path, "r", encoding="utf-8") as file:
    danish_words = [line.strip() for line in file.readlines()]

# print(len(danish_words))
# 60509

# Ensure the output directory exists
output_dir = "output_test"
output_dir_images = os.path.join(output_dir, "images")
labels_file = os.path.join(output_dir, "labels.json")

os.makedirs(output_dir_images, exist_ok=True)

# read output_dir labels.json if it exists
if os.path.exists(labels_file):
    with open(labels_file, "r", encoding="utf-8") as f:
        labels_dict = json.load(f)
        print(f"Loaded {labels_file}")
else:
    labels_dict = {}


# Demonstration
danish_words = danish_words[:10]
counter = 0
for index, word in enumerate(danish_words):
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

    counter += 1

    # print progress after every 1000 images
    if counter % 100 == 0:
        print(f"Generated {counter} images")


"""
# labels.json
{
    "img_1.jpg": "I",
    "img_2.jpg": "am",
    "img_3.jpg": "a",
    "img_4.jpg": "Jedi",
    "img_5.jpg": "!",
    ...
}
"""

# save dict_index as json file
with open(labels_file, "w", encoding="utf-8") as f:
    json.dump(labels_dict, f, ensure_ascii=False, indent=4)
