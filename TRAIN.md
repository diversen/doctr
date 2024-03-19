# Install

    # needed
    sudo apt-get install -y libpangocairo-1.0-0
    
    # some extra fonts. You may not need this
    sudo apt-get install ttf-mscorefonts-installer
    sudo apt-get install fonts-freefont-ttf
    sudo apt-get install -y fonts-ebgaramond

    git clone https://github.com/mindee/doctr
    cd doctr
    virtualenv venv

    pip install -r requirements-trdg.txt
    pip install -e . --upgrade
    pip install -r references/requirements.txt

# generate synth images 

Will output training data to /home/dennis/d/validation. It will first generate at least 10 random words from wikipedia and then generate images for each word. The images will be stored in /home/dennis/d/train. The number of images of each word is controlled by the --num-images-per-word flag.

    python generate-img.py --num-words 250000 --num-images-per-word 2 --output-dir train-data

Restarting from a word:

    python generate-img.py --num-words 250000 --num-images-per-word 2 --output-dir train-data --begin-word fremvisning

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
