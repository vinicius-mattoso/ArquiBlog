from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

# Carregamento uma única vez
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def descrever_imagem(imagem_path):
    """
    Gera uma descrição textual da imagem fornecida usando o modelo BLIP.
    """
    image = Image.open(imagem_path).convert('RGB')
    inputs = processor(image, return_tensors="pt")

    with torch.no_grad():
        out = model.generate(**inputs, max_length=50)  # Evita gerar descrições muito longas por acidente
    descricao = processor.decode(out[0], skip_special_tokens=True)
    return descricao
