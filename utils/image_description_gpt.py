import base64
import mimetypes

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from utils.config import get_config


def carregar_imagem_base64(imagem_path):
    mime_type, _ = mimetypes.guess_type(imagem_path)
    with open(imagem_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_string}"


def descrever_imagem(imagem_path, api_key):
    config = get_config()
    model_config = config["models"]
    prompt_config = config["prompts"]["image_analysis"]
    imagem_base64 = carregar_imagem_base64(imagem_path)

    chat = ChatOpenAI(
        model=model_config["image_analysis"],
        temperature=model_config["vision_temperature"],
        openai_api_key=api_key,
        max_tokens=model_config["vision_max_tokens"]
    )

    messages = [
        SystemMessage(content=prompt_config["system_prompt"]),
        HumanMessage(
            content=[
                {"type": "image_url", "image_url": {"url": imagem_base64}},
                {"type": "text", "text": prompt_config["user_prompt"]}
            ]
        )
    ]

    response = chat.invoke(messages)
    return response.content
