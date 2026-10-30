class Cobranca:

    def __init__(
        self,
        grupo,
        gerente,
        link_grupo,
        link_demandas,
        mensagem
    ):

        self.grupo = grupo
        self.gerente = gerente
        self.link_grupo = link_grupo
        self.link_demandas = link_demandas
        self.mensagem = mensagem

        self.status = "Pendente"
        self.linha_tabela = None

    def __str__(self):

        return (
            f"{self.gerente}"
        )