import base64
import mimetypes
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

def carregar_imagem_base64(imagem_path):
    mime_type, _ = mimetypes.guess_type(imagem_path)
    with open(imagem_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_string}"

def descrever_imagem(imagem_path, api_key):
    imagem_base64 = carregar_imagem_base64(imagem_path)
    
    chat = ChatOpenAI(
        model="gpt-4-turbo",  # novo modelo com suporte a visão
        temperature=0.2,
        openai_api_key=api_key,
        max_tokens=500
    )

    messages = [
        SystemMessage(content="Você é um arquiteto especialista em design de interiores. Analise a imagem e descreva com detalhes técnicos e sensoriais o estilo, os materiais e a função do ambiente."),
        HumanMessage(
            content=[
                {"type": "image_url", "image_url": {"url": imagem_base64}},
                {"type": "text", "text": "Descreva o ambiente como se fosse publicar no Instagram de um escritório de arquitetura sofisticado."}
            ]
        )
    ]

    response = chat.invoke(messages)
    return response.content
