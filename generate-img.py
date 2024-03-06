import random
import os
from trdg.generators import GeneratorFromStrings
from PIL import Image

# Common font paths on Linux systems (adjust according to your system)
fonts = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",  # Monospaced variant
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",  # Assuming Ubuntu Mono Regular
]

text_colors = [
    "#000000",  # Black
    "#FFFFFF",  # White
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


# background_types = [0, 1, 2, 3]  # Different background types
distorsion_types = [0, 1, 2]  # Different distortion types

# Path to the Danish words file
words_file_path = "venv/lib/python3.10/site-packages/trdg/dicts/da.txt"

# Read all Danish words from the file
with open(words_file_path, "r", encoding="utf-8") as file:
    danish_words = [line.strip() for line in file.readlines()]

# Ensure the output directory exists
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Use first 10 words for demonstration
danish_words = danish_words[:200]
for index, word in enumerate(danish_words):
    font = random.choice(fonts)
    text_color = random.choice(text_colors)
    distorsion_type = random.choice(distorsion_types)
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
        img_path = os.path.join(output_dir, f"image_{index}.png")
        img.save(img_path)
        break  # Exit after saving the first image