from pathlib import Path
from utils.app_path import CONFIG_DIR

CONFIG_FILE = CONFIG_DIR / "browser.conf"


def salvar_navegador(navegador):
    CONFIG_FILE.write_text(
        navegador,
        encoding="utf-8"
    )


def carregar_navegador():

    if not CONFIG_FILE.exists():
        return "automatico"

    return CONFIG_FILE.read_text(
        encoding="utf-8"
    ).strip()