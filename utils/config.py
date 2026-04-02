import os
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

import yaml
from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_DIR / "config.yaml"

load_dotenv(ROOT_DIR / ".env")


@lru_cache(maxsize=1)
def get_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Arquivo de configuracao nao encontrado: {CONFIG_PATH}")

    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        return yaml.safe_load(config_file)


def save_config(config):
    with CONFIG_PATH.open("w", encoding="utf-8") as config_file:
        yaml.safe_dump(
            config,
            config_file,
            allow_unicode=False,
            sort_keys=False,
            default_flow_style=False,
        )
    get_config.cache_clear()


def get_openai_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY nao definida no .env")
    return api_key


def get_channel_options():
    return get_config()["channels"]


def get_public_brand_settings():
    config = get_config()
    return {
        "product_name": config["app"]["product_name"],
        "office_name": config["app"]["office_name"],
        "tagline": config["brand"]["tagline"],
        "voice_style": config["brand"]["voice_style"],
        "persona": config["brand"]["persona"],
        "objective": config["brand"]["objective"],
        "default_channel": config["app"]["default_channel"],
    }


def update_public_brand_settings(payload):
    config = deepcopy(get_config())

    field_map = {
        ("app", "office_name"): "office_name",
        ("brand", "tagline"): "tagline",
        ("brand", "voice_style"): "voice_style",
        ("brand", "persona"): "persona",
        ("brand", "objective"): "objective",
        ("app", "default_channel"): "default_channel",
    }

    for (section, key), payload_key in field_map.items():
        if payload_key in payload and payload[payload_key]:
            config[section][key] = str(payload[payload_key]).strip()

    if config["app"]["default_channel"] not in config["channels"]:
        raise ValueError("Canal padrao invalido.")

    save_config(config)
    return get_public_brand_settings()
