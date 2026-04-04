import json
import os
import re
from datetime import datetime

from langchain_openai import OpenAI

from utils.config import get_config, get_openai_api_key
from utils.image_description_gpt import descrever_imagem
from utils.prompt_builder import montar_prompt


def build_llm(config, api_key):
    model_config = config["models"]
    return OpenAI(
        temperature=model_config["text_temperature"],
        model=model_config["text_generation"],
        openai_api_key=api_key,
    )


def _save_history_entry(entry, historico_path):
    historico = []
    if os.path.exists(historico_path):
        try:
            with open(historico_path, "r", encoding="utf-8") as arquivo:
                historico = json.load(arquivo)
        except json.JSONDecodeError:
            print("[ALERTA] Historico corrompido. Um novo sera criado.")

    historico.append(entry)
    with open(historico_path, "w", encoding="utf-8") as arquivo:
        json.dump(historico, arquivo, ensure_ascii=False, indent=4)


def _count_words(text):
    return len(re.findall(r"\S+", text))


def _trim_to_word_limit(text, max_words):
    words = re.findall(r"\S+", text)
    if len(words) <= max_words:
        return text.strip()

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    kept_sentences = []

    for sentence in sentences:
        candidate = " ".join(kept_sentences + [sentence]).strip()
        if _count_words(candidate) <= max_words:
            kept_sentences.append(sentence)
        else:
            break

    if kept_sentences:
        return " ".join(kept_sentences).strip()

    trimmed = " ".join(words[:max_words]).strip()
    return trimmed.rstrip(",;:-")


def _enforce_channel_word_limit(text, config, channel_key):
    if channel_key not in {"blog", "linkedin"}:
        return text.strip()

    max_words = config["channels"][channel_key]["output"]["max_words"]
    normalized_text = text.strip()

    if _count_words(normalized_text) <= max_words:
        return normalized_text

    return _trim_to_word_limit(normalized_text, max_words)


def gerar_post_completo(frases, imagem_path, channel_key="blog"):
    config = get_config()

    if channel_key not in config["channels"]:
        raise ValueError("Canal de conteudo invalido.")

    if not frases or not any(frase for frase in frases):
        raise ValueError("Frases fornecidas estao vazias.")

    if not os.path.exists(imagem_path):
        raise FileNotFoundError(f"Imagem '{imagem_path}' nao encontrada.")

    api_key = get_openai_api_key()

    try:
        descricao_imagem = descrever_imagem(imagem_path, api_key=api_key)
        print(descricao_imagem)
    except Exception as exc:
        descricao_imagem = "Descricao automatica indisponivel."
        print(f"[ERRO] Falha ao gerar descricao da imagem: {exc}")

    prompt = montar_prompt(frases, descricao_imagem, config, channel_key)

    try:
        texto = build_llm(config, api_key).invoke(prompt)
    except Exception as exc:
        raise RuntimeError(f"Erro ao gerar texto com LLM: {exc}") from exc

    texto = _enforce_channel_word_limit(texto, config, channel_key)

    agora = datetime.now()
    timestamp = agora.strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"post_{timestamp}.txt"
    pasta_posts = "posts"
    os.makedirs(pasta_posts, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_posts, nome_arquivo)

    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)

    historico_path = os.path.join(pasta_posts, "historico.json")
    novo_registro = {
        "data_hora": agora.strftime("%d/%m/%Y %H:%M:%S"),
        "canal": channel_key,
        "frases": frases,
        "imagem": os.path.relpath(imagem_path),
        "descricao_imagem": descricao_imagem,
        "arquivo_txt": caminho_arquivo,
        "modelo_texto": config["models"]["text_generation"],
        "modelo_imagem": config["models"]["image_analysis"],
    }
    _save_history_entry(novo_registro, historico_path)

    return {"texto": texto, "registro": novo_registro}


def gerar_post(frases, imagem_path, channel_key="blog"):
    return gerar_post_completo(frases, imagem_path, channel_key)["texto"]
