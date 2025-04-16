import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="ArquiBlog | Geração Inteligente de Posts",
    page_icon="🏛️",
    layout="wide"
)

st.title("🏛️ ArquiBlog – Geração Inteligente de Posts de Arquitetura")
st.markdown("""
Bem-vindo ao **ArquiBlog**, a plataforma que utiliza **inteligência artificial** para transformar seus projetos em **posts completos para o blog do escritório**.

Com apenas uma imagem e algumas frases descritivas, o ArquiBlog gera automaticamente um texto profissional com:

- Título e introdução criativa
- Descrição técnica e estética
- Destaques do projeto
- Sugestões de tags e chamadas para redes sociais

Ideal para arquitetos e escritórios que querem manter um blog ativo sem precisar escrever tudo manualmente!

""")

st.subheader("📸 Exemplo de entrada")
img = Image.open("assets/exemplo_projeto.jpg")
st.image(img, caption="Montagem de um projeto real de fachada contemporânea", use_container_width=True)

st.markdown("➡️ Acesse a aba *Gerador de Post* no menu à esquerda para começar.")
