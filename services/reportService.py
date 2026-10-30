from openpyxl import Workbook
from utils.app_path import REPORTS_DIR


class ReportService:

    @staticmethod
    def gerar_relatorio_erros(erros):

        wb = Workbook()

        ws = wb.active
        ws.title = "Erros"

        ws.append([
            "Gerente",
            "Grupo",
            "Motivo"
        ])

        for erro in erros:

            ws.append([
                erro["gerente"],
                erro["grupo"],
                erro["erro"]
            ])

        wb.save(
            REPORTS_DIR / "erros.xlsx"
        )