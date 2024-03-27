import torch
from doctr.models import crnn_vgg16_bn
from doctr.datasets import VOCABS


reco_model = crnn_vgg16_bn(pretrained=True, pretrained_backbone=False, vocab=VOCABS["danish"])
trained_model = "/home/dennis/doctr/crnn_vgg16_bn_20240326-123828.pt"
reco_params = torch.load(trained_model, map_location="cpu")
reco_model.load_state_dict(reco_params)

# doctr-torch-crnn_vgg16_bn-danish-v1/pytorch_model.bin
torch.save(reco_model.state_dict(), "/home/dennis/doctr-torch-crnn_vgg16_bn-danish-v1/pytorch_model.bin")