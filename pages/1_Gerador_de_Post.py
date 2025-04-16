import streamlit as st
from PIL import Image, ImageOps
from utils.generator import gerar_post

st.set_page_config(page_title="Gerar Post | ArquiBlog")
st.title("🛠️ Gerador de Post para Blog de Arquitetura")

st.markdown("Preencha as informações abaixo para gerar um post contínuo, pronto para o blog.")

# Upload da imagem
uploaded_file = st.file_uploader("📤 Envie a imagem do projeto", type=["jpg", "jpeg", "png"])

# Inputs de frases
st.markdown("**📝 Descreva seu projeto em até 3 frases (mínimo 1):**")
frase1 = st.text_input("Frase 1 – Conceito do projeto")
frase2 = st.text_input("Frase 2 – Materiais, estilo ou soluções")
frase3 = st.text_input("Frase 3 – Localização, público-alvo ou desafios")

# Botão de ação
if st.button("🚀 Gerar post"):
    if not uploaded_file:
        st.warning("Por favor, envie uma imagem do projeto.")
    elif not any([frase1, frase2, frase3]):
        st.warning("Preencha pelo menos uma das frases para contextualizar o projeto.")
    else:
        with st.spinner("Gerando texto com inteligência artificial..."):
            # Nome seguro para a imagem
            imagem_nome = getattr(uploaded_file, "name", "imagem_sem_nome.jpg")

            # Geração do post
            texto_gerado = gerar_post([frase1, frase2, frase3], imagem_nome)

            st.success("✅ Post gerado com sucesso!")

            # Redimensiona a imagem com proporção para exibição clara
            imagem = Image.open(uploaded_file)
            imagem_redimensionada = ImageOps.contain(imagem, (700, 1000))

            st.markdown("### 📸 Imagem do Projeto:")
            st.image(imagem_redimensionada, caption="Visual do projeto", use_container_width=False)

            st.markdown("### 🧾 Texto Gerado:")
            st.markdown(texto_gerado, unsafe_allow_html=True)

            st.download_button("📥 Baixar como .txt", data=texto_gerado, file_name="post_arquiblog.txt")
