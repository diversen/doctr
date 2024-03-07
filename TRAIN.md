# train

    python references/recognition/train_pytorch.py crnn_vgg16_bn --vocab danish --train_path train --val_path val --epochs 5 

# Resume 

    python references/recognition/train_pytorch.py crnn_vgg16_bn --vocab danish --train_path train --val_path val --epochs 5 --resume ./crnn_vgg16_bn_DATE_TIME.pt
