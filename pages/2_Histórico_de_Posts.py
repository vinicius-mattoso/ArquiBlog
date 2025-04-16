import streamlit as st
import json
import os

st.set_page_config(page_title="Histórico de Posts | ArquiBlog")
st.title("📚 Histórico de Posts Gerados")

historico_path = os.path.join("posts", "historico.json")

if not os.path.exists(historico_path):
    st.info("Nenhum post foi gerado ainda.")
else:
    with open(historico_path, "r", encoding="utf-8") as f:
        historico = json.load(f)

    for item in reversed(historico):
        st.markdown("----")
        st.markdown(f"**🕒 Gerado em:** {item['data_hora']}")
        st.markdown(f"**🖼️ Arquivo de imagem:** `{item['imagem']}`")

        st.markdown("**🧾 Frases usadas:**")
        for i, frase in enumerate(item["frases"], start=1):
            st.markdown(f"- {frase}")

        st.markdown(f"📄 **Arquivo gerado:** `{item['arquivo_txt']}`")

        if os.path.exists(item["arquivo_txt"]):
            with open(item["arquivo_txt"], "r", encoding="utf-8") as f:
                conteudo = f.read()
                with st.expander("🔍 Visualizar texto"):
                    st.markdown(conteudo)
                    st.download_button("📥 Baixar novamente", conteudo, file_name=os.path.basename(item["arquivo_txt"]))