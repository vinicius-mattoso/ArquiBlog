import streamlit as st
import json
import os
from PIL import Image

st.set_page_config(page_title="Histórico de Posts | ArquiBlog")
st.title("📚 Histórico de Posts Gerados")

historico_path = os.path.join("posts", "historico.json")

if not os.path.exists(historico_path):
    st.info("Nenhum post foi gerado ainda.")
else:
    with open(historico_path, "r", encoding="utf-8") as f:
        historico = json.load(f)

    if not historico:
        st.info("Nenhum registro encontrado no histórico.")
    else:
        for item in reversed(historico):
            st.markdown("----")
            col1, col2 = st.columns([1, 2])

            with col1:
                if os.path.exists(item["imagem"]):
                    try:
                        st.image(Image.open(item["imagem"]), caption="Imagem do projeto", use_container_width=True)
                    except Exception:
                        st.warning("Imagem não pôde ser carregada.")
                else:
                    st.warning("Imagem não encontrada.")

            with col2:
                st.markdown(f"**🕒 Gerado em:** `{item['data_hora']}`")
                st.markdown(f"**📁 Arquivo de imagem:** `{item['imagem']}`")

                st.markdown("**🧾 Frases fornecidas:**")
                for i, frase in enumerate(item["frases"], start=1):
                    st.markdown(f"- {frase}")

                if "descricao_imagem" in item:
                    with st.expander("🧠 Descrição gerada da imagem"):
                        st.markdown(item["descricao_imagem"])

                st.markdown(f"📄 **Arquivo de texto:** `{item['arquivo_txt']}`")

                if os.path.exists(item["arquivo_txt"]):
                    with open(item["arquivo_txt"], "r", encoding="utf-8") as f_txt:
                        conteudo = f_txt.read()
                        with st.expander("🔍 Visualizar texto gerado"):
                            st.markdown(conteudo)
                            st.download_button(
                                "📥 Baixar .txt",
                                conteudo,
                                file_name=os.path.basename(item["arquivo_txt"]),
                                use_container_width=True
                            )

                if "modelo_usado" in item:
                    st.markdown(f"🤖 **Modelo utilizado:** `{item['modelo_usado']}`")
