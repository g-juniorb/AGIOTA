from openpyxl import load_workbook

from models.cobranca import Cobranca
from utils.dataUtils import obter_saudacao


class ExcelService:

    @staticmethod
    def extrair_gerente(grupo):

        return (
            grupo
            .replace("Time ", "")
            .replace(
                " | Chat de Grupo | Microsoft Teams",
                ""
            )
            .strip()
        )

    @staticmethod
    def carregar_cobrancas(caminho_excel):

        wb = load_workbook(caminho_excel)

        aba_dados = wb[wb.sheetnames[0]]
        aba_mensagem = wb[wb.sheetnames[1]]

        mensagem_template = (
            aba_mensagem["A1"].value
        )

        cobrancas = []

        for linha, row in enumerate(
            aba_dados.iter_rows(min_row=2),
            start=0
        ):

            envia = row[0].value

            if str(envia).upper() != "S":
                continue

            celula_grupo = row[1]

            grupo = celula_grupo.value

            link_grupo = None

            if celula_grupo.hyperlink:
                link_grupo = (
                    celula_grupo.hyperlink.target
                )
            if link_grupo:

                link_grupo = (
                    link_grupo.replace(
                        "https://teams.microsoft.com/",
                        "https://teams.microsoft.com/_#/"
                    )
                )

            link_demandas = row[2].value

            gerente = (
                ExcelService.extrair_gerente(
                    grupo
                )
            )

            mensagem = (
                mensagem_template
                .replace(
                    "#Saudacao",
                    obter_saudacao()
                )
                .replace(
                    "#LinkDemandas",
                    str(link_demandas)
                )
            )

            cobranca = Cobranca(
                grupo=grupo,
                gerente=gerente,
                link_grupo=link_grupo,
                link_demandas=link_demandas,
                mensagem=mensagem
            )

            cobranca.linha_tabela = linha

            cobrancas.append(
                cobranca
            )

        return cobrancas