import json
import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

from utils.config import (
    get_channel_options,
    get_config,
    get_public_brand_settings,
    update_public_brand_settings,
)
from utils.generator import gerar_post_completo


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
POSTS_DIR = BASE_DIR / "posts"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["JSON_AS_ASCII"] = False


def _allowed_file(filename):
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def _read_history():
    history_path = POSTS_DIR / "historico.json"
    if not history_path.exists():
        return []

    with history_path.open("r", encoding="utf-8") as history_file:
        try:
            history = json.load(history_file)
        except json.JSONDecodeError:
            return []

    items = []
    channel_options = get_channel_options()
    for item in reversed(history):
        image_rel = item.get("imagem", "")
        text_rel = item.get("arquivo_txt", "")
        image_name = Path(image_rel).name if image_rel else ""
        text_name = Path(text_rel).name if text_rel else ""
        text_content = ""
        text_path = BASE_DIR / text_rel if text_rel else None
        if text_path and text_path.exists():
            text_content = text_path.read_text(encoding="utf-8")

        channel_key = item.get("canal", "blog")
        channel_label = channel_options.get(channel_key, {}).get("label", channel_key.title())

        items.append(
            {
                "data_hora": item.get("data_hora"),
                "canal": channel_key,
                "canal_label": channel_label,
                "frases": item.get("frases", []),
                "descricao_imagem": item.get("descricao_imagem", ""),
                "imagem_url": f"/uploads/{image_name}" if image_name else None,
                "imagem_nome": image_name,
                "arquivo_txt_nome": text_name,
                "arquivo_txt_url": f"/posts/{text_name}" if text_name else None,
                "texto": text_content,
                "modelo_texto": item.get("modelo_texto") or item.get("modelo_usado"),
                "modelo_imagem": item.get("modelo_imagem"),
            }
        )
    return items


@app.get("/")
def index():
    config = get_config()
    return render_template(
        "index.html",
        brand_settings=get_public_brand_settings(),
        channels=get_channel_options(),
        initial_history=_read_history()[:6],
        product_name=config["app"]["product_name"],
    )


@app.get("/api/bootstrap")
def bootstrap():
    return jsonify(
        {
            "brand_settings": get_public_brand_settings(),
            "channels": get_channel_options(),
            "history": _read_history(),
        }
    )


@app.post("/api/generate")
def generate():
    imagem = request.files.get("image")
    channel_key = request.form.get("channel", get_public_brand_settings()["default_channel"])
    frases = [
        request.form.get("phrase1", ""),
        request.form.get("phrase2", ""),
        request.form.get("phrase3", ""),
    ]

    if imagem is None or not imagem.filename:
        return jsonify({"error": "Envie uma imagem do projeto."}), 400

    if not _allowed_file(imagem.filename):
        return jsonify({"error": "Formato de imagem inválido. Use JPG, JPEG ou PNG."}), 400

    if not any(frase.strip() for frase in frases):
        return jsonify({"error": "Preencha ao menos uma frase para contextualizar o projeto."}), 400

    UPLOAD_DIR.mkdir(exist_ok=True)
    safe_name = secure_filename(imagem.filename)
    unique_name = f"projeto_{Path(safe_name).stem}_{os.urandom(4).hex()}{Path(safe_name).suffix.lower()}"
    image_path = UPLOAD_DIR / unique_name
    imagem.save(image_path)

    try:
        result = gerar_post_completo(frases, str(image_path), channel_key=channel_key)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

    history = _read_history()
    latest_item = history[0] if history else None
    return jsonify(
        {
            "message": "Conteúdo gerado com sucesso.",
            "text": result["texto"],
            "history_item": latest_item,
        }
    )


@app.get("/api/history")
def history():
    return jsonify({"items": _read_history()})


@app.post("/api/settings")
def update_settings():
    payload = request.get_json(silent=True) or {}
    try:
        settings = update_public_brand_settings(payload)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400
    return jsonify({"message": "Configurações atualizadas.", "settings": settings})


@app.get("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)


@app.get("/posts/<path:filename>")
def post_file(filename):
    return send_from_directory(POSTS_DIR, filename, as_attachment=False)


if __name__ == "__main__":
    app.run(debug=True)
