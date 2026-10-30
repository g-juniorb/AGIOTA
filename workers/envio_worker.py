from PySide6.QtCore import QThread
from PySide6.QtCore import Signal
import time
from playwright.sync_api import sync_playwright

from utils.app_path import PROFILE_DIR
from utils.browser_utils import localizar_navegador
from pages.teamsPage import TeamsPage
from services.teams_service import TeamsService
from exceptions.teams_exception import (
    UsuarioNaoEstaNoGrupoError
)

class EnvioWorker(QThread):

    progresso = Signal(int)
    log = Signal(str)
    status = Signal(int, str)
    finalizado = Signal(list)

    def __init__(self, cobrancas, modo_visual):

        super().__init__()

        self.cobrancas = cobrancas
        self.erros = []
        self.modo_visual = modo_visual
        self.parar = False

    def parar_execucao(self):
        self.parar = True

    def run(self):
        print("=== COBRANCAS NO WORKER ===")

        for i, cobranca in enumerate(self.cobrancas):
            print(i, cobranca.gerente)

        total = len(self.cobrancas)

        chrome_path = localizar_navegador()

        with sync_playwright() as p:

            browser = p.chromium.launch_persistent_context(
                user_data_dir=PROFILE_DIR,
                executable_path=chrome_path,
                headless=not self.modo_visual
            )

            page = browser.new_page()

            teams_page = TeamsPage(page)

            teams_page.abrir()

            service = TeamsService(
                teams_page
            )

            for indice, cobranca in enumerate(
                self.cobrancas
            ):

                if self.parar:
                    break
                self.log.emit("====================================================")
                self.log.emit(
                    f"📨 Iniciando cobrança para: "
                    f"{cobranca.gerente}"
                )

                sucesso = False
                ultimo_erro = ""

                for tentativa in range(1, 4):

                    try:

                        self.status.emit(
                            cobranca.linha_tabela,
                            f"Tentando ({tentativa}/3)"
                        )

                        self.log.emit(
                            f"🔄 Tentativa {tentativa}/3"
                        )

                        service.enviar_para_grupo(
                            cobranca
                        )

                        self.log.emit(
                            "✅ Cobrança enviada com sucesso."
                        )
                        self.log.emit(
                            "===================================================="
                        )

                        self.status.emit(
                            cobranca.linha_tabela,
                            "Sucesso"
                        )

                        sucesso = True

                        break

                    except UsuarioNaoEstaNoGrupoError as e:

                        ultimo_erro = self.formatar_erro(e)

                        self.log.emit(
                            "❌ Não foi possível acessar o grupo do Teams."
                        )

                        self.log.emit(
                            f"Motivo: {ultimo_erro}"
                        )

                        sucesso = False

                        break

                    except Exception as e:

                        ultimo_erro = self.formatar_erro(e)

                        self.log.emit(
                            f"⚠️ Tentativa {tentativa}/3 falhou."
                        )

                        self.log.emit(
                            f"Motivo: {ultimo_erro}"
                        )

                        if tentativa < 3:

                            self.log.emit(
                                "🔁 Nova tentativa em 5 segundos..."
                            )

                            time.sleep(5)

                if not sucesso:

                    self.status.emit(
                        cobranca.linha_tabela,
                        "Erro"
                    )

                    self.log.emit(
                        "⛔ Cobrança não enviada."
                    )

                    self.erros.append({
                        "grupo": cobranca.grupo,
                        "gerente": cobranca.gerente,
                        "erro": ultimo_erro,
                        "cobranca": cobranca
                    })

            percentual = int(
                ((indice + 1) / total) * 100
            )

            self.progresso.emit(
                percentual
            )

            browser.close()
            print("TOTAL ERROS:", len(self.erros))
            self.finalizado.emit(
                self.erros
            )

    def formatar_erro(
        self,
        erro
    ):

        erro = str(erro)

        if "autocomplete-picker-item" in erro:
            return (
                "Não foi possível localizar a sugestão "
                "de menção do Teams."
            )

        if "chat you're not in" in erro:
            return (
                "Usuário logado não participa deste grupo do Teams."
            )

        if "Timeout" in erro:
            return (
                "Tempo limite excedido durante a operação."
            )

        return erro