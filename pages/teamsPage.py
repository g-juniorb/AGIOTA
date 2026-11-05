# pages/teams_page.py

import time
from pages.basePage import BasePage
from exceptions.teams_exception import (UsuarioNaoEstaNoGrupoError)

class TeamsPage(BasePage):

    URL = "https://teams.cloud.microsoft/"

    def abrir(self):
        self.page.goto(self.URL)

    def aguardar_carregamento(self):
        self.page.wait_for_timeout(3000)

    def abrir_grupo(
        self,
        link_grupo
    ):

        self.page.goto(link_grupo)

        self.page.wait_for_load_state()

        self.page.wait_for_timeout(10000)

        popup = self.page.locator(
            "h2"
        ).filter(
            has_text="We"
        )
        if popup.count() > 0:

            raise UsuarioNaoEstaNoGrupoError(
                "Usuário logado não participa deste grupo do Teams."
            )

    def limpar_campo_mensagem(self):

        caixa = self.page.locator(
            "[contenteditable='true']"
        )

        caixa.evaluate(
            "element => element.textContent = ''"
        )

    def mencionar_usuario(
        self,
        nome_usuario
    ):

        caixa = self.page.locator(
            "[contenteditable='true']"
        )

        caixa.click()

        caixa.type(
            f"@{nome_usuario}",
            delay=50
        )

        self.page.wait_for_timeout(
            1500
        )

        sugestao = self.page.locator(
            '[data-tid*="autocomplete-picker-item"]'
        ).first

        sugestao.wait_for(
            timeout=2000
        )

        sugestao.click()

        self.page.wait_for_timeout(
            1000
        )

    def inserir_link(
        self,
        url,
        texto=None
    ):

        texto = texto or url

        # Simula um paste com HTML para forçar a criação de um link real,
        # já que o auto-link do Teams falha em URLs longas/codificadas.
        self.page.evaluate(
            """([html, texto]) => {
                const dt = new DataTransfer();
                dt.setData('text/html', html);
                dt.setData('text/plain', texto);
                const alvo = document.querySelector(
                    "[contenteditable='true']"
                );
                alvo.dispatchEvent(new ClipboardEvent('paste', {
                    clipboardData: dt,
                    bubbles: true,
                    cancelable: true
                }));
            }""",
            [f'<a href="{url}">{texto}</a>', texto]
        )

        self.page.wait_for_timeout(500)

    def _digitar_com_link(
        self,
        trecho,
        link
    ):

        link = str(link) if link else None

        if link and link in trecho:

            antes, depois = trecho.split(link, 1)

            self.page.keyboard.insert_text(antes)
            self.inserir_link(link)
            self.page.keyboard.insert_text(depois)

        else:
            self.page.keyboard.insert_text(trecho)

    def enviar_mensagem_com_mencao(
        self,
        cobranca
    ):

        caixa = self.page.locator(
            "[contenteditable='true']"
        )

        caixa.click()

        texto_antes, texto_depois = (
            cobranca.mensagem.split(
                "#Gerente",
                1
            )
        )

        # Primeira parte
        self._digitar_com_link(
            texto_antes,
            cobranca.link_demandas
        )

        self.page.wait_for_timeout(1000)

        # Menção
        self.mencionar_usuario(
            cobranca.gerente.title()
        )

        self.page.wait_for_timeout(1000)

        # Segunda parte
        self._digitar_com_link(
            texto_depois,
            cobranca.link_demandas
        )

        self.page.keyboard.type(" ")
        self.page.wait_for_timeout(3000)

        # Produção
        self.page.keyboard.press("Enter")
        time.sleep(1)
        self.page.keyboard.press("Enter")
        time.sleep(1)
        self.page.keyboard.press("Enter")
        time.sleep(1)
 
    def escrever_mensagem(self, mensagem):


        caixa = self.page.locator("[contenteditable='true']")

        caixa.fill(mensagem, timeout=10000)

        self.page.wait_for_timeout(5000)
       # self.page.keyboard.press("Enter")
       # self.page.keyboard.press("Enter")
       # time.sleep(1)
       # self.page.keyboard.press("Enter")


    def tirar_evidencia(self, caminho):

        self.page.screenshot(
            path=caminho,
            full_page=True
        )