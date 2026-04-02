import os
from datetime import datetime

import streamlit as st
from PIL import Image, ImageOps

from utils.generator import gerar_post


st.set_page_config(page_title="Gerar Post | ArquiBlog")
st.title("Gerador de Post para Blog de Arquitetura")
st.markdown("Preencha as informacoes abaixo para gerar um post continuo, pronto para o blog.")

uploaded_file = st.file_uploader("Envie a imagem do projeto", type=["jpg", "jpeg", "png"])

st.markdown("**Descreva seu projeto em ate 3 frases (minimo 1):**")
frase1 = st.text_input("Frase 1 - Conceito do projeto")
frase2 = st.text_input("Frase 2 - Materiais, estilo ou solucoes")
frase3 = st.text_input("Frase 3 - Localizacao, publico-alvo ou desafios")

if st.button("Gerar post"):
    if not uploaded_file:
        st.warning("Por favor, envie uma imagem do projeto.")
    elif not any([frase1, frase2, frase3]):
        st.warning("Preencha pelo menos uma das frases para contextualizar o projeto.")
    else:
        with st.spinner("Gerando texto com inteligencia artificial..."):
            upload_dir = "uploads"
            os.makedirs(upload_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            imagem_temp_path = os.path.join(upload_dir, f"projeto_{timestamp}{ext}")

            with open(imagem_temp_path, "wb") as arquivo:
                arquivo.write(uploaded_file.read())

            try:
                texto_gerado = gerar_post([frase1, frase2, frase3], imagem_temp_path)

                st.success("Post gerado com sucesso.")

                imagem = Image.open(imagem_temp_path)
                imagem_redimensionada = ImageOps.contain(imagem, (700, 1000))

                st.markdown("### Imagem do Projeto")
                st.image(imagem_redimensionada, caption="Visual do projeto", use_container_width=False)

                st.markdown("### Texto Gerado")
                st.markdown(texto_gerado, unsafe_allow_html=True)

                st.download_button(
                    "Baixar como .txt",
                    data=texto_gerado,
                    file_name="post_arquiblog.txt"
                )
            except Exception as exc:
                st.error(f"Erro ao gerar o post: {exc}")
