# Install

    # needed
    sudo apt-get install -y libpangocairo-1.0-0
    
    # some extra fonts. These are already included in ./fonts
    # sudo apt-get install ttf-mscorefonts-installer
    # sudo apt-get install fonts-freefont-ttf
    # sudo apt-get install -y fonts-ebgaramond

    git clone https://github.com/mindee/doctr
    cd doctr
    virtualenv venv

    pip install -r requirements-trdg.txt
    pip install -e . --upgrade
    pip install -r references/requirements.txt

# generate synth images 

**generate some words from wikipedia**

This will generate at least `1000` words in a sqlite3 `database.db` placed in `output`. 
Using docTR vocab `danish` and wiki lang `da` 

    python generate-words.py --num-words 1000 --output-dir output --vocab danish --lang da

**generate images from database words**

In the `output/images` generate `1000 x 2` images using `da` words. 

    python generate-img.py --num-words 1000 --num-images-per-word 2 --output-dir output --lang da

**generate labels**

    python generate-labels.py --output-dir output --num-words 10 --lang da

# train danish from scratch

    python references/recognition/train_pytorch.py crnn_vgg16_bn --vocab danish --train_path train-data --val_path validation-data --epochs 5 

# resume from french model

    python references/recognition/train_pytorch.py crnn_vgg16_bn --max-chars 32 --vocab danish --train_path train-data --val_path validation-data --epochs 5 --pretrained

# resume on local trained model

    python references/recognition/train_pytorch.py crnn_vgg16_bn --max-chars 32 --vocab danish --train_path train-data --val_path validation-data --epochs 5 --pretrained --resume crnn_vgg16_bn_20240316-233300.pt

# resume on crn_vgg16_bn 

    python references/recognition/train_pytorch.py crnn_vgg16_bn --vocab danish --train_path train-data --val_path validation-data --epochs 1 --resume /home/dennis/.cache/doctr/models/crnn_vgg16_bn-9762b0b0.pt

# push to hub

 python references/recognition/train_pytorch.py crnn_vgg16_bn --max-chars 32 --vocab danish --train_path train-data --val_path validation-data --epochs 1 --pretrained --resume crnn_vgg16_bn_20240317-095746.pt --push-to-hub --name doctr-torch-crnn_vgg16_bn-danish-v1

# example convert from .pt to .bin

    python convert.py


