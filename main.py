import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from utils.resource_path import resource_path
from gui.main_window import MainWindow


app = QApplication(sys.argv)

app.setApplicationName("GIGI")
app.setOrganizationName("@JR")
app.setWindowIcon(
    QIcon(resource_path("gui/assets/icon.ico"))
)

app.setStyle("Fusion")

app.setStyleSheet("""
QMainWindow {
    background-color: qlineargradient(
        x1:0,
        y1:0,
        x2:1,
        y2:1,
        stop:0 #0B1F4D,
        stop:0.40 #161616,
        stop:0.70 #1E1E1E,
        stop:1 #003DA5
    );
}

QWidget {
    color: white;
    background-color: qradialgradient(
        cx:0.5,
        cy:0.5,
        radius:1.2,
        stop:0 #1E1E1E,
        stop:0.75 #1E1E1E,
        stop:1 #003DA5
    );
}

/* Labels */

QLabel {
    color: white;
    font-size: 12px;
}

/* Campos */

QLineEdit {
    background-color: #252526;
    color: white;
    border: 1px solid #404040;
    border-radius: 6px;
    padding: 6px;
}

/* Log */

QTextEdit {
    background-color: #252526;
    color: white;
    border: 1px solid #404040;
    border-radius: 6px;
}

/* Botões padrão */

QPushButton {
    background-color: #003DA5;
    color: white;
    border-radius: 6px;
    padding: 8px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #0052CC;
}

QPushButton:pressed {
    background-color: #002D7A;
}

QPushButton:disabled {
    background-color: #555555;
    color: #BBBBBB;
}

/* Tabela */

QTableWidget {
    background-color: #252526;
    color: white;
    border: 1px solid #404040;
    gridline-color: #404040;
    selection-background-color: #003DA5;
}

QHeaderView::section {
    background-color: #003DA5;
    color: white;
    font-weight: bold;
    border: none;
    padding: 8px;
}

/* Barra de progresso */

QProgressBar {
    background-color: #252526;
    border: 1px solid #404040;
    border-radius: 6px;
    text-align: center;
    color: white;
}

QProgressBar::chunk {
    background-color: #F9C400;
    border-radius: 5px;
}
""")

window = MainWindow()
window.show()

sys.exit(app.exec())