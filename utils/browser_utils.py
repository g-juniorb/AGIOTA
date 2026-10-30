import platform
from pathlib import Path

from utils.settings import carregar_navegador


def localizar_navegador():

    preferencia = carregar_navegador()

    sistema = platform.system()

    if sistema == "Windows":

        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]

        edge_paths = [
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        ]

    elif sistema == "Darwin":

        chrome_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        ]

        edge_paths = [
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
        ]

    else:
        return None

    if preferencia == "chrome":

        for caminho in chrome_paths:
            if Path(caminho).exists():
                return caminho

    elif preferencia == "edge":

        for caminho in edge_paths:
            if Path(caminho).exists():
                return caminho

    else:

        for caminho in chrome_paths:
            if Path(caminho).exists():
                return caminho

        for caminho in edge_paths:
            if Path(caminho).exists():
                return caminho

    return None