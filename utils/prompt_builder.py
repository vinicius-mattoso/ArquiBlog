def montar_prompt(frases, descricao_imagem, config, channel_key):
    app_config = config["app"]
    brand_config = config["brand"]
    writing_config = config["prompts"]["writing"]
    channel_config = config["channels"][channel_key]

    frases_formatadas = "\n".join([f"- {frase}" for frase in frases if frase])
    global_guidelines = "\n".join(
        [f"- {guideline}" for guideline in writing_config["global_style_guidelines"]]
    )
    channel_guidelines = "\n".join(
        [f"- {guideline}" for guideline in channel_config["style_guidelines"]]
    )
    content_structure = "\n".join(
        [f"- {item}" for item in channel_config["content_structure"]]
    )
    output_config = channel_config["output"]

    prompt = f"""
Voce e um {brand_config["persona"]}, criando conteudos para o escritorio {app_config["office_name"]}.

Contexto da marca:
- Voz da marca: {brand_config["voice_style"]}
- Objetivo principal: {brand_config["objective"]}
- Canal de saida: {channel_config["label"]} ({channel_config["output_label"]})
- Descricao do canal: {channel_config["description"]}

Diretrizes globais:
{global_guidelines}

Diretrizes especificas do canal:
{channel_guidelines}

Estrutura esperada:
{content_structure}

Parametros finais:
- Texto entre {output_config["min_words"]} e {output_config["max_words"]} palavras
- Nunca ultrapasse o limite maximo de {output_config["max_words"]} palavras
- CTA: {output_config["cta_style"]}
- Emojis: {output_config["emoji_policy"]}
- Hashtags de referencia: {output_config["hashtags_hint"]}

Descricao automatica da imagem:
"{descricao_imagem}"

Frases fornecidas pelo escritorio:
{frases_formatadas}

Entregue o conteudo final pronto para publicacao, sem explicacoes extras.
"""
    return prompt
