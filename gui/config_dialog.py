from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton
)

from utils.settings import (
    salvar_navegador,
    carregar_navegador
)


class ConfigDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Configurações"
        )

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel("Navegador:")
        )

        self.combo = QComboBox()

        self.combo.addItems([
            "automatico",
            "chrome",
            "edge"
        ])

        navegador = carregar_navegador()

        self.combo.setCurrentText(
            navegador
        )

        layout.addWidget(
            self.combo
        )

        btn_salvar = QPushButton(
            "Salvar"
        )

        btn_salvar.clicked.connect(
            self.salvar
        )

        layout.addWidget(
            btn_salvar
        )

        self.setLayout(
            layout
        )

    def salvar(self):

        salvar_navegador(
            self.combo.currentText()
        )

        self.accept()