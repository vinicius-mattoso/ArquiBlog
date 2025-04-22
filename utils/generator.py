import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import OpenAI
# from utils.image_description import descrever_imagem
from utils.image_description_gpt import descrever_imagem
from utils.prompt_builder import montar_prompt

# Carrega variáveis do .env
load_dotenv()

# Validação da chave de API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY não definida no .env")

# Instância do modelo
llm = OpenAI(
    temperature=0.7,
    model="gpt-3.5-turbo-instruct",
    openai_api_key=OPENAI_API_KEY
)

def gerar_post(frases, imagem_path):
    """
    Gera um post de blog com base nas frases fornecidas e na imagem enviada.
    """
    # Verificação de entradas
    if not frases or not any(frases):
        raise ValueError("Frases fornecidas estão vazias.")
    
    if not os.path.exists(imagem_path):
        raise FileNotFoundError(f"Imagem '{imagem_path}' não encontrada.")
    
    try:
        # descricao_imagem = descrever_imagem(imagem_path)
        descricao_imagem = descrever_imagem(imagem_path, api_key=OPENAI_API_KEY)
        print(descricao_imagem)
    except Exception as e:
        descricao_imagem = "Descrição automática indisponível."
        print(f"[ERRO] Falha ao gerar descrição da imagem: {e}")

    # Gera o prompt completo com as frases + descrição visual
    prompt = montar_prompt(frases, descricao_imagem)

    try:
        texto = llm.invoke(prompt)
    except Exception as e:
        raise RuntimeError(f"Erro ao gerar texto com LLM: {e}")
    
    # Salvar o texto gerado
    agora = datetime.now()
    timestamp = agora.strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"post_{timestamp}.txt"
    pasta_posts = "posts"
    os.makedirs(pasta_posts, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_posts, nome_arquivo)

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(texto)

    # Atualizar histórico
    historico_path = os.path.join(pasta_posts, "historico.json")
    novo_registro = {
    "data_hora": agora.strftime("%d/%m/%Y %H:%M:%S"),
    "frases": frases,
    "imagem": os.path.relpath(imagem_path),
    "descricao_imagem": descricao_imagem,
    "arquivo_txt": caminho_arquivo,
    "modelo_usado": "gpt-4-turbo"
}

    historico = []
    if os.path.exists(historico_path):
        try:
            with open(historico_path, "r", encoding="utf-8") as f:
                historico = json.load(f)
        except json.JSONDecodeError:
            print("[ALERTA] Histórico corrompido. Um novo será criado.")

    historico.append(novo_registro)
    with open(historico_path, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=4)

    return texto
