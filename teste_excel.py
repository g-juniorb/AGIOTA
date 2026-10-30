from services.excel_service import ExcelService

cobrancas = ExcelService.carregar_cobrancas(
    "gui/assets/MsgGerente.xlsx"
)

for cobranca in cobrancas:

    print("=" * 50)

    print("GERENTE:")
    print(cobranca.gerente)

    print("\nLINK GRUPO:")
    print(cobranca.link_grupo)

    print("\nLINK DEMANDAS:")
    print(cobranca.link_demandas)

    print("\nMENSAGEM:")
    print(cobranca.mensagem)