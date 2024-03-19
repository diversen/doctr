import os
import random


def get_fonts():
    """
    Get all .ttf files in ./fonts
    """
    fonts = []
    for root, dirs, files in os.walk("./fonts"):
        for file in files:
            if file.endswith(".ttf"):
                fonts.append(os.path.join(root, file))

    return fonts


fonts = get_fonts()
couri_fonts = [font for font in fonts if "Couri" in font]
type_writer_fonts = [font for font in fonts if "SpecialElite-Regular" in font]

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

# Fonts configuration
def get_use_fonts():    
    if random.randint(0, 5) == 0:
        return couri_fonts
    elif random.randint(0, 5) == 1:  # Fixed conditional to ensure it's a unique case
        return type_writer_fonts
    else:
        return fonts

# Other configurations
def get_font():
    use_fonts = get_use_fonts()
    return random.choice(use_fonts)

def get_text_color():
    return random.choice(text_colors)

def get_size():
    return random.randint(32, 124)

def get_space_width():
    return random.uniform(0.5, 2.5)

def get_character_spacing():
    return random.randint(0, 25)

def get_skewing_angle():
    return random.randint(0, 5)

def get_blur():
    return random.choice([0, 1, 2])

def get_distorsion_orientation():
    return random.choice([0, 1])

def get_background_type():
    return random.choice([0, 1, 2])

def transform_word(word):
    word_cased = word
    if random.randint(0, 9) == 0:
        word_cased = word.upper()

    return word_cased

# language = "da" 
distorsion_type = 0
orientation = 0
