import os
import json

# create 'image' dir if it does not exist
if not os.path.exists("images"):
    os.makedirs("images")

# Copy all images from output/ to images/
os.system("cp -f output/* images/")

# Remove "train" dir and create it again
if os.path.exists("train"):
    os.system("rm -rf train")

# create dirs train/images
os.makedirs("train/images", exist_ok=True)

# Remove val dir and create it again
if os.path.exists("val"):
    os.system("rm -rf val")

os.makedirs("val/images", exist_ok=True)

# Get all images from images/
images = os.listdir("images")

# Calculate 80% of the images
eighty_percent = int(0.8 * len(images))

# Copy 80% of the images to train/
for image in images[:eighty_percent]:
    os.system(f"cp images/{image} train/images")

# Copy 20% of the images to val/
for image in images[eighty_percent:]:
    os.system(f"cp images/{image} val/images")

