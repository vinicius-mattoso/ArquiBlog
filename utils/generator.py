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

def montar_prompt(frases):
    frases_formatadas = "\n".join([f"- {f}" for f in frases if f])
    prompt = f"""
Você é um redator especialista em arquitetura, escrevendo para o blog do escritório Pistache Arquitetura. Seu estilo é emocional, leve, envolvente, com vocabulário acessível e técnico na medida certa. Escreva como se estivesse conversando com o leitor, transmitindo sensações, memórias e experiências ligadas aos ambientes.

Objetivo: Criar um post de blog encantador, que conte a história do projeto de forma fluida, conectando o espaço à vida de quem o habita.

Diretrizes:
- Comece com um título criativo e sensível (em destaque)
- Introduza o projeto com emoção, falando da proposta, do uso do espaço e da experiência desejada
- Siga com a descrição técnica (materiais, texturas, layout, móveis, iluminação) de forma leve e envolvente
- Termine com uma reflexão inspiradora e um call to action sutil (ex: “qual peça da sua casa traz as melhores lembranças?”)
- O tom deve ser gentil, visual, sensorial — evite parecer publicitário ou formal demais
- Nunca mencione o nome do arquivo de imagem
- Use emojis pontualmente, como já usado nas redes do escritório (ex: ✨, 💛,💚,🤍, 🏡)
- Finalize com hashtags alinhadas ao conteúdo
- As ultimas 100 palavras deve ser as hashtags

Fontes de referência de estilo e tom:
- @pistachearquitetura no Instagram
- Exemplo de tom: “Cada detalhe conta uma história e reflete a essência do lar. 💛”
- Exemplo de frase técnica leve: “A base neutra, com materiais naturais, cria um ambiente atemporal e acolhedor...”
- Exemplo de linguagem emocional: “Transformar memórias em design: esse foi o ponto de partida…”

Informações fornecidas para esse post:
{frases_formatadas}

Requisitos técnicos:
- O texto deve ter entre 800 e 1000 palavras
- Não utilize intertítulos visíveis
- O conteúdo deve estar pronto para ser publicado, sem necessidade de ajustes

Capriche na coesão e na estética do texto, como se estivesse escrevendo diretamente para os seguidores do Instagram que agora chegaram ao blog.
"""
    return prompt


def gerar_post(frases, imagem_nome):
    frases_formatadas = "\n".join([f"- {f}" for f in frases if f])
#     prompt = f"""
# Você é um redator especializado em arquitetura. Com base nas informações abaixo, escreva um post de blog com estilo fluido, contínuo e bem redigido, pronto para ser publicado em um site.

# Formato desejado:
# - Um título criativo no topo
# - Introdução com apelo emocional e contexto do projeto
# - Seção técnica (materiais, estilo, decisões projetuais)
# - Encerramento com tom inspirador e com um call to action para entrar em contato para saber mais sobre esses e outros projetos
# - Sem intertítulos visíveis
# - Não cite o nome da imagem em nenhum momento
# - Não esqueça de colocar as hastags

# Informações fornecidas:
# {frases_formatadas}

# O texto deve ter entre 800 e 1000 palavras, bem coeso, com vocabulário acessível e envolvente.
# """
    if not frases or not any(frases):
        raise ValueError("Frases fornecidas estão vazias.")
    
    prompt = montar_prompt(frases)

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
