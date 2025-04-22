def montar_prompt(frases, descricao_imagem):
    frases_formatadas = "\n".join([f"- {f}" for f in frases if f])
    prompt = f"""
Você é um redator especialista em arquitetura de interiores, criando conteúdos envolventes e sofisticados para o blog do escritório Pistache Arquitetura.

Sua missão é gerar um post de blog com linguagem emocional, técnica e sensorial, que transforme a imagem analisada em uma narrativa inspiradora, conectando o projeto ao estilo de vida dos moradores.

**Formato do conteúdo esperado:**
- Um título criativo no topo (sem marcar como título)
- Abertura emocional (contexto do projeto, sentimentos que ele desperta)
- Desenvolvimento com descrição técnica: materiais, texturas, layout, soluções inteligentes
- Encerramento reflexivo e com um convite suave para o leitor interagir (call to action)
- Ao final, inclua **hashtags relevantes**, separadas por espaço, com até 100 palavras. Ex: #arquitetura #interiores #pistachearquitetura

**Importante:**
- Não insira intertítulos
- Use um vocabulário acessível, elegante e natural
- Escreva de forma contínua, sem parecer que foram colados trechos
- Use emojis pontualmente como nos posts do Instagram (ex: ✨ 💛 🤍)
- Não mencione o nome do arquivo da imagem

---

**Descrição automática da imagem:**
"{descricao_imagem}"

**Frases fornecidas pelo escritório para complementar o contexto:**
{frases_formatadas}

---

Gere um texto com entre 850 e 1000 palavras, bem coeso e pronto para publicação.
"""
    return prompt
