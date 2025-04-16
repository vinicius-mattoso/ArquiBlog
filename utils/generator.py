import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY não definida no .env")

llm = OpenAI(
    temperature=0.7,
    model="gpt-3.5-turbo-instruct",
    openai_api_key=OPENAI_API_KEY
)

def gerar_post(frases, imagem_nome):
    frases_formatadas = "\n".join([f"- {f}" for f in frases if f])
    prompt = f"""
Você é um redator especializado em arquitetura contemporânea. Com base nas informações abaixo, escreva um post de blog com estilo fluido, contínuo e bem redigido, pronto para ser publicado em um site.

Formato desejado:
- Um título criativo no topo
- Introdução com apelo emocional e contexto do projeto
- Seção técnica (materiais, estilo, decisões projetuais)
- Encerramento com tom inspirador e com um call to action para entrar em contato para saber mais sobre esses e outros projetos
- Sem intertítulos visíveis
- Não cite o nome da imagem em nenhum momento

Informações fornecidas:
{frases_formatadas}

O texto deve ter entre 500 e 800 palavras, bem coeso, com vocabulário acessível e envolvente.
"""

    # Gera o texto
    # texto = llm(prompt)
    texto = llm.invoke(prompt)

    # Salvar o texto
    agora = datetime.now()
    timestamp = agora.strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"post_{timestamp}.txt"
    caminho_arquivo = os.path.join("posts", nome_arquivo)

    os.makedirs("posts", exist_ok=True)
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(texto)

    # Registrar no histórico
    historico_path = os.path.join("posts", "historico.json")
    novo_registro = {
        "data_hora": agora.strftime("%d/%m/%Y %H:%M:%S"),
        "frases": frases,
        "imagem": imagem_nome,
        "arquivo_txt": caminho_arquivo
    }

    historico = []
    if os.path.exists(historico_path):
        with open(historico_path, "r", encoding="utf-8") as f:
            historico = json.load(f)

    historico.append(novo_registro)
    with open(historico_path, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=4)

    return texto
