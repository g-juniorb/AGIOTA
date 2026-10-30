class TeamsService:

    def __init__(
        self,
        teams_page
    ):
        self.teams_page = teams_page

    def enviar_para_grupo(
        self,
        cobranca
    ):

        self.teams_page.abrir_grupo(
            cobranca.link_grupo
        )

        self.teams_page.enviar_mensagem_com_mencao(cobranca)
        #self.teams_page.escrever_mensagem(
        #    cobranca.mensagem
        #)