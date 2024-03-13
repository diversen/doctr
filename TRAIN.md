# generate synth images 

Will output training data to /home/dennis/d/validation. It will first generate at least 10 random words from wikipedia and then generate images for each word. The images will be stored in /home/dennis/d/train. The number of images of each word is controlled by the --num-images-per-word flag.

    python generate-img.py --num-words 10 --num-images-per-word 1 --output-dir /home/dennis/d/generate-test --word-list ~/d/words-test.json 

# train danish from scratch

    python references/recognition/train_pytorch.py crnn_vgg16_bn --vocab danish --train_path train --val_path val --epochs 5 

# resume from french model

    python references/recognition/train_pytorch.py crnn_vgg16_bn --max-chars 32 --vocab multilingual --train_path ~/d/train --val_path ~/d/validation --epochs 2 --pretrained --workers 4

# train multilingual

    python references/recognition/train_pytorch.py crnn_vgg16_bn --max-chars 32 --vocab multilingual --train_path ~/d/train --val_path ~/d/validation --epochs 5 --resume /home/dennis/.cache/doctr/models/crnn_vgg16_bn-9762b0b0.pt --early_stop

# resume on crn_vgg16_bn 

    python references/recognition/train_pytorch.py crnn_vgg16_bn --vocab multilingual --train_path ~/d/train --val_path ~/d/validation --epochs 1 --resume /home/dennis/.cache/doctr/models/crnn_vgg16_bn-9762b0b0.pt

    

python references/recognition/train_pytorch.py crnn_vgg16_bn --max-chars 32 --vocab multilingual --train_path ~/d/train --val_path ~/d/validation --epochs 5 --resume ./crnn_vgg16_bn_20240312-123338.pt --early-stop


# Train status

Validation loss: 0.0599899 (Exact: 91.91% | Partial: 93.28%)
Validation loss: 0.047381 (Exact: 93.61% | Partial: 94.75%)
Validation loss: 0.0422745 (Exact: 94.42% | Partial: 95.43%) 

# Hacking



