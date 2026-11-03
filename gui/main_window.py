from PySide6.QtWidgets import *
from PySide6.QtWidgets import QHeaderView
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
import os
import shutil
from workers.envio_worker import EnvioWorker
from services.excel_service import ExcelService
from services.reportService import ReportService
from utils.browser_utils import localizar_navegador
from utils.app_path import CONFIG_DIR, PROFILE_DIR, REPORTS_DIR
from utils.resource_path import resource_path
from gui.config_dialog import ConfigDialog


class MainWindow(QMainWindow):
    


    def __init__(self):

        super().__init__()

        self.cobrancas = []
        self.falhas = []
        self.modo_visual = False

        self.setWindowTitle(
            "GIGI - Cobrador"
        )
        self.setWindowIcon(
            QIcon(resource_path("gui/assets/icon.ico"))
        )

        

        self.worker = None

        self.sucessos = 0
        self.erros = 0

        self.resize(
            650,
            650
        )


        self.criar_tela()
        self.validar_conexao_teams()


    def criar_tela(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        layout = QVBoxLayout()
        layout.setSpacing(2)
    

         # =====================================
         # STATUS TEAMS
         # =====================================
        
        linha_teams = QHBoxLayout()
                
    
        self.lbl_status_icon = QLabel()
        
        self.lbl_status = QLabel(
            "Desconectado"
        )
        

        self.btn_login = QPushButton(
            
        )
        self.btn_login.setIcon(
            QIcon(resource_path("gui/assets/teams.png"))
        )

        self.btn_login.setIconSize(
            QSize(24, 24)
        )
        self.btn_login.setText(
            " Conectar ao Teams"
        )
        self.btn_login.setStyleSheet("""
        QPushButton {
            background-color: #6264A7;
            color: white;
            border-radius: 8px;
            padding: 10px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #7B83EB;
        }

        QPushButton:pressed {
            background-color: #4D4FB8;
        }
        """)

        self.btn_login.clicked.connect(
            self.login_teams
        )

        self.btn_config = QPushButton(
            "⚙️"
        )

        self.btn_config.clicked.connect(
            self.abrir_configuracoes
        )
        linha_teams = QHBoxLayout()

        status_layout = QVBoxLayout()

        status_layout.addWidget(
            self.lbl_status
        )

        linha_teams.addLayout(
            status_layout
        )

        linha_teams.addStretch()

        linha_teams.addWidget(
            self.btn_login
        )

        layout.addLayout(
            linha_teams
        )

        # =====================================
        # LOGO
        # =====================================

        self.lbl_logo = QLabel()
        self.lbl_logo.setAlignment(
            Qt.AlignCenter #type: ignore
        )

        self.lbl_logo.setStyleSheet("""
        margin-bottom: 0px;
        margin-top: 0px;
        """)
 


        pixmap = QPixmap(resource_path("gui/assets/logo.png")) #type: ignore

        self.lbl_logo.setPixmap(
            pixmap.scaled(
                350,
                180,
                Qt.KeepAspectRatio, #type: ignore
                Qt.SmoothTransformation #type: ignore
            )
        )

        self.lbl_logo.setAlignment(
            Qt.AlignCenter #type: ignore
        )

        layout.addWidget(
            self.lbl_logo
        )

       

        # arquivo

        linha = QHBoxLayout()

        self.txt_arquivo = QLineEdit()

        btn_arquivo = QPushButton(
            "Selecionar Excel"
        )
        btn_arquivo.setText(
            "📂 Selecionar Excel"
        )

        btn_arquivo.clicked.connect(
            self.selecionar_excel
        )

        linha.addWidget(
            self.txt_arquivo
        )

        linha.addWidget(
            btn_arquivo
        )

        layout.addLayout(
            linha
        )

        # indicadores

        linha_ind = QHBoxLayout()

        self.lbl_total = QLabel(
            "Total: 0"
        )

        self.lbl_sucesso = QLabel(
            "Sucesso: 0"
        )

        self.lbl_erro = QLabel(
            "Erro: 0"
        )
        self.lbl_total.setStyleSheet("""
        background-color:rgba(37,37,38,180);
        border:1px solid #404040;
        border-radius:8px;
        padding:10px;
        font-weight:bold;
        color:#F9C400;
        """)

        self.lbl_sucesso.setStyleSheet("""
        background-color:rgba(37,37,38,180);
        border:1px solid #404040;
        border-radius:8px;
        padding:10px;
        font-weight:bold;
        color:#28C76F;
        """)

        self.lbl_erro.setStyleSheet("""
        background-color:rgba(37,37,38,180);
        border:1px solid #404040;
        border-radius:8px;
        padding:10px;
        font-weight:bold;
        color:#EA5455;
        """)

        linha_ind.addWidget(
            self.lbl_total
        )

        linha_ind.addWidget(
            self.lbl_sucesso
        )

        linha_ind.addWidget(
            self.lbl_erro
        )

        layout.addLayout(
            linha_ind
        )

        # barra

        self.progress = QProgressBar()

        self.progress.setStyleSheet("""
        QProgressBar {
            border: 1px solid #444;
            border-radius: 5px;
            text-align:center;
            background:rgba(37,37,38,180);
            color:white;
        }

        QProgressBar::chunk {
            background-color:#F9C400;
            border-radius:4px;
        }
        """)
        layout.addWidget(
            self.progress
        )

        # tabela

        self.tabela = QTableWidget()
        self.tabela.setStyleSheet("""
        QTableWidget {
            background-color: rgba(37,37,38,180);
            color: white;
            gridline-color: #404040;
            selection-background-color: #003DA5;
        }

        QHeaderView::section {
            background-color: #003DA5;
            color: white;
            font-weight: bold;
            padding: 6px;
            border: none;
        }
        """)

        self.tabela.setColumnCount(3)

        self.tabela.setHorizontalHeaderLabels([
            "Gerente",
            "Mensagem",
            "Status"
        ])

        layout.addWidget(
            self.tabela
        )
        self.tabela.horizontalHeader().setStretchLastSection(True)

        self.tabela.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.Stretch # type: ignore
        )

        self.tabela.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.Stretch # type: ignore
        )

        self.tabela.horizontalHeader().setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents # type: ignore
        )


        # botão

        self.btn_enviar = QPushButton(
            "🚀 Iniciar Cobrança"
        )
        self.btn_enviar.setStyleSheet("""
        QPushButton {
            background-color:#F9C400;
            color:#003DA5;
            font-size:14px;
            font-weight:bold;
            border:none;
            border-radius:8px;
            padding:12px;
        }

        QPushButton:hover {
            background-color:#FFD84D;
        }

        QPushButton:pressed {
            background-color:#E6B800;
        }
        """)
        self.btn_enviar.clicked.connect(
            self.iniciar_envio
        )

        self.btn_parar = QPushButton(
            "🛑 Parar Execução"
        )

        self.btn_parar.setEnabled(False)

        self.btn_reexecutar = QPushButton(
            "🔄 Reexecutar Falhas"
        )

        self.btn_reexecutar.setEnabled(False)

        self.btn_reexecutar.clicked.connect(
            self.reexecutar_falhas
        )

        self.btn_exportar = QPushButton(
                "📦 Exportar Evidências"
            )
    
        self.btn_exportar.clicked.connect(
            self.exportar_evidencias
        )

        self.btn_exportar.setEnabled(False)

        linha_botoes = QHBoxLayout()

        linha_botoes.addWidget(
            self.btn_enviar
        )

        linha_botoes.addWidget(
            self.btn_parar
        )

        linha_botoes.addWidget(
            self.btn_reexecutar
        )

        linha_botoes.addWidget(
            self.btn_exportar
        )

        layout.addLayout(
            linha_botoes
        )

        self.btn_parar.setEnabled(False)

        self.btn_parar.clicked.connect(
            self.parar_execucao
        )

        #Estilos botoes
        self.btn_enviar.setStyleSheet("""
        QPushButton {
            background-color: #F9C400;
            color: #003DA5;
            font-weight: bold;
            border-radius: 6px;
            padding: 10px;
            font-size: 12px;
        }

        QPushButton:hover {
            background-color: #FFD84D;
        }

        QPushButton:pressed {
            background-color: #E6B800;
        }
        """)

        for btn in [
            self.btn_login,
            self.btn_exportar,
            self.btn_enviar,
            self.btn_parar,
            self.btn_reexecutar,
            self.btn_config
        ]:
            btn.setCursor(Qt.PointingHandCursor) #type: ignore

        # log

        self.log_text = QTextEdit()

        self.log_text.setReadOnly(True)

        layout.addWidget(
            self.log_text
        )
        self.footer = QLabel(
            "GIGI Cobrador v1.0.1 | Desenvolvido por G. Junior | © 2026"
        )

        self.footer.setAlignment(
            Qt.AlignCenter #type: ignore
        )

        self.footer.setStyleSheet("""
        color: #888888;
        font-size: 10px;
        padding-top: 8px;
        """)

        rodape_layout = QHBoxLayout()

        self.chk_visualizacao = QCheckBox(
            "👁️ Modo Assistido"
        )

        self.chk_visualizacao.setChecked(False)

        self.chk_visualizacao.stateChanged.connect(
            self.alternar_visualizacao
        )

        self.chk_visualizacao.setStyleSheet("""
        QCheckBox {
            color: #888888;
            font-size: 10px;
        }

        QCheckBox::indicator {
            width: 12px;
            height: 12px;
        }
        """)

        self.footer.setStyleSheet("""
        color: #888888;
        font-size: 10px;
        """)

        self.btn_modelo = QPushButton(
            "📥 Baixar Modelo"
        )

        self.btn_modelo.clicked.connect(
            self.baixar_modelo
        )
        self.btn_modelo.setStyleSheet("""
        QPushButton {
            background: transparent;
            border: none;
            color: #888888;
            font-size: 10px;
        }

        QPushButton:hover {
            color: #F9C400;
        }
        """)

        rodape_layout.addWidget(
            self.btn_config
        )

        rodape_layout.addWidget(
            self.chk_visualizacao
        )

        rodape_layout.addSpacing(10)

        rodape_layout.addWidget(
            self.btn_modelo
        )

        rodape_layout.addStretch()

        rodape_layout.addWidget(
            self.footer
        )

        layout.addLayout(
            rodape_layout
        )

        central.setLayout(
            layout
        )

    def selecionar_excel(self):

        arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Excel",
            "",
            "*.xlsx"
        )

        if not arquivo:
            return

        # Limpa tabela anterior
        self.tabela.setRowCount(0)

        # Limpa lista carregada anteriormente
        self.cobrancas = []

        # Reseta contadores
        self.lbl_total.setText("Total: 0")
        self.lbl_sucesso.setText("Sucesso: 0")
        self.lbl_erro.setText("Erro: 0")

        # Limpa barra de progresso
        self.progress.setValue(0)

        # Limpa log (opcional)
        self.log_text.clear()

        self.txt_arquivo.setText(
            arquivo
        )

        service = ExcelService()

        self.cobrancas = (
            service.carregar_cobrancas(
                arquivo
            )
        )

        self.carregar_tabela()

    def carregar_tabela(self):

        self.tabela.setRowCount(
            len(self.cobrancas)
        )

        for linha, cobranca in enumerate(
                self.cobrancas):

            cobranca.linha_tabela = linha
            self.tabela.setItem(
                linha,
                0,
                QTableWidgetItem(
                    cobranca.gerente
                )
            )

            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    cobranca.mensagem
                )
            )

            item_status = QTableWidgetItem("Pendente")

            item_status.setTextAlignment(
                Qt.AlignCenter #type: ignore
            )

            self.tabela.setItem(
                linha,
                2,
                item_status
            )
        
        self.lbl_total.setText(
            f"Total: {len(self.cobrancas)}"
        )

    def adicionar_log(self, texto):

        self.log_text.append(
            texto
        )

    def teams_conectado(self):

        if not PROFILE_DIR.exists():
            return False

        try:
            return any(PROFILE_DIR.iterdir())
        except Exception:
            return False
    def validar_conexao_teams(self):

        if PROFILE_DIR.exists():

            if len(os.listdir(PROFILE_DIR)) > 0:

                self.lbl_status.setText(
                    "🟢 Teams Conectado"
                )

                self.lbl_status.setStyleSheet("""
                padding: 6px 12px;
                font-weight: bold;
                color: #28C76F;
                """)

                self.btn_login.setText(
                    "🔄 Atualizar Login"
                )
                self.btn_login.setStyleSheet("""
                QPushButton {
                    background-color: #3A3A3A;
                    color: white;
                    border-radius: 6px;
                    padding: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #505050;
                }
                """)

                return


        self.lbl_status.setText(
            "🔴 Teams Desconectado"
        )

        self.lbl_status.setStyleSheet("""
        padding: 6px 12px;
        font-weight: bold;
        color: #EA5455;
        """)

        self.btn_login.setText(
            "🔐 Conectar ao Teams"
        )
        self.btn_login.setStyleSheet("""
        QPushButton {
            background-color: #6264A7;
            color: white;
            border-radius: 8px;
            padding: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #7B83EB;
        }
        """)
    def login_teams(self):

        from playwright.sync_api import sync_playwright

        chrome_path = localizar_navegador()

        if not chrome_path:

            QMessageBox.warning(
                self,
                "Navegador não encontrado",
                "Chrome ou Edge não foram encontrados.\n\n"
                "Instale o Google Chrome ou selecione "
                "manualmente o executável do navegador."
            )

            self.selecionar_navegador()

            return

        with sync_playwright() as p:
            print("Navegador:", chrome_path)
            browser = (
                p.chromium.launch_persistent_context(
                    user_data_dir=str(PROFILE_DIR),
                    executable_path=chrome_path,
                    headless=False
                )
            )

            page = browser.new_page()

            page.goto(
                "https://teams.cloud.microsoft"
            )

            QMessageBox.information(
                self,
                "Login Teams",
                "Realize o login no Teams.\n\nApós finalizar, feche o navegador clicando em OK na modal."
            )

        self.validar_conexao_teams()

    def atualizar_status(
        self,
        linha,
        status):
        item_status = QTableWidgetItem(status)

        item_status.setTextAlignment(
            Qt.AlignCenter #type: ignore
        )

        self.tabela.setItem(
            linha,
            2,
            item_status
        )

        self.cobrancas[linha].status = status

        if status == "Sucesso":

            self.sucessos += 1

            self.lbl_sucesso.setText(
                f"✅ Sucesso: {self.sucessos}"
            )

        if status == "Erro":

            self.erros += 1

            self.lbl_erro.setText(
                f"❌ Erro: {self.erros}"
            )

    def iniciar_envio(self):

        if len(self.cobrancas) == 0:

            QMessageBox.warning(
                self,
                "Aviso",
                "Nenhuma cobrança carregada."
            )

            return
        if not self.teams_conectado():

            QMessageBox.warning(
                self,
                "Teams não conectado",
                "Conecte-se ao Teams antes de iniciar o envio."
            )

            return

        self.sucessos = 0
        self.erros = 0

        self.lbl_sucesso.setText(
            "Sucesso: 0"
        )

        self.lbl_erro.setText(
            "Erro: 0"
        )

        self.progress.setValue(0)

        self.btn_enviar.setEnabled(
            False
        )

        self.btn_parar.setEnabled(
            True
        )

        self.adicionar_log(
            f"🚀 Iniciando processamento de {len(self.cobrancas)} cobrança(s)..."
        )

        print("=== COBRANCAS NO MAIN ===")

        for i, cobranca in enumerate(self.cobrancas):
            print(i, cobranca.gerente)
            
        self.worker = EnvioWorker(
            self.cobrancas,
            self.modo_visual
        )

        self.worker.progresso.connect(
            self.progress.setValue
        )

        self.worker.log.connect(
            self.adicionar_log
        )

        self.worker.status.connect(
            self.atualizar_status
        )

        self.worker.finalizado.connect(
            self.envio_finalizado
        )

        self.worker.start()

    def parar_execucao(self):

        if self.worker:

            self.worker.parar_execucao()

            self.btn_enviar.setEnabled(True)

            self.btn_parar.setEnabled(False)

            self.adicionar_log(
                "🛑 Execução interrompida."
            )
    def envio_finalizado(self, erros):

        self.falhas = erros
        self.btn_enviar.setEnabled(True)

        self.btn_parar.setEnabled(False)
        self.btn_exportar.setEnabled(True)

        self.adicionar_log("🏁 Processo finalizado")

        self.adicionar_log("📊 Resumo da Execução:")

        self.adicionar_log(
            f"   📨 Total processado: {len(self.cobrancas)}"
        )

        self.adicionar_log(
            f"   ✅ Sucessos: {self.sucessos}"
        )

        self.adicionar_log(
            f"   ❌ Erros: {self.erros}"
        )
        if len(self.falhas) > 0:

            self.btn_reexecutar.setEnabled(True)

        else:

            self.btn_reexecutar.setEnabled(False)

        if len(erros) > 0:

            ReportService.gerar_relatorio_erros(
                erros
            )

        self.adicionar_log(
            f"📄 Relatório de erros gerado em: "
            f"{REPORTS_DIR / 'erros.xlsx'}"
        )
    def selecionar_navegador(self):

        arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Navegador",
            "",
            "Executáveis (*.exe)"
        )

        if not arquivo:
            return

        arquivo_config = CONFIG_DIR / "browser_path.txt"

        arquivo_config.write_text(
            arquivo,
            encoding="utf-8"
        )

        QMessageBox.information(
            self,
            "Sucesso",
            "Navegador salvo com sucesso."
        )
    def reexecutar_falhas(self):

        if not self.falhas:

            QMessageBox.information(
                self,
                "Reexecução",
                "Não existem falhas para reprocessar."
            )

            return

        cobrancas_falha = [
            erro["cobranca"]
            for erro in self.falhas
        ]

        # Limpa falhas antigas
        self.falhas = []

        # Reseta contadores da reexecução
        self.sucessos = 0
        self.erros = 0

        self.lbl_sucesso.setText(
            "✅ Sucesso: 0"
        )

        self.lbl_erro.setText(
            "❌ Erro: 0"
        )

        self.progress.setValue(0)

        self.btn_reexecutar.setEnabled(False)

        self.adicionar_log(
            f"🔄 Reexecutando {len(cobrancas_falha)} falha(s)..."
        )

        self.worker = EnvioWorker(
            cobrancas_falha,
            self.modo_visual
        )

        self.worker.progresso.connect(
            self.progress.setValue
        )

        self.worker.log.connect(
            self.adicionar_log
        )

        self.worker.status.connect(
            self.atualizar_status
        )

        self.worker.finalizado.connect(
            self.envio_finalizado
        )

        self.worker.start()

    def alternar_visualizacao(self):

        self.modo_visual = (
            self.chk_visualizacao.isChecked()
        )

    def baixar_modelo(self):

        destino, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Modelo",
            "Modelo_Cobrancas.xlsx",
            "*.xlsx"
        )

        if not destino:
            return

        shutil.copy(
            resource_path(
                "gui/assets/MsgGerente.xlsx"
            ),
            destino
        )

        QMessageBox.information(
            self,
            "Sucesso",
            "Modelo salvo com sucesso."
        )

    def abrir_configuracoes(self):

        dialog = ConfigDialog()

        dialog.exec()

    def salvar_log(self, pasta):

        with open(
            pasta / "Log_Execucao.txt",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                self.log_text.toPlainText()
            )

    def exportar_evidencias(self):

        from pathlib import Path
        from datetime import datetime
        from openpyxl import Workbook

        pasta_destino = QFileDialog.getExistingDirectory(
            self,
            "Selecionar pasta destino"
        )

        if not pasta_destino:
            return

        pasta = (
            Path(pasta_destino)
            / f"Evidencias_GIGI_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        pasta.mkdir(
            parents=True,
            exist_ok=True
        )

        # Log
        with open(
            pasta / "Log_Execucao.txt",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                self.log_text.toPlainText()
            )

        # Planilha resultado
        wb = Workbook()

        ws = wb.active

        ws.title = "Resultado"

        ws.append([
            "Gerente",
            "Grupo",
            "Status"
        ])

        for cobranca in self.cobrancas:

            ws.append([
                cobranca.gerente,
                cobranca.grupo,
                getattr(
                    cobranca,
                    "status",
                    "Pendente"
                )
            ])

        wb.save(
            pasta / "Planilha_Resultado.xlsx"
        )

        # Resumo
        with open(
            pasta / "Resumo.txt",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                f"""GIGI - Resumo de Execução

    Total: {len(self.cobrancas)}
    Sucessos: {self.sucessos}
    Erros: {self.erros}
    """
            )

        QMessageBox.information(
            self,
            "Exportação",
            f"Evidências exportadas com sucesso.\n\n{pasta}"
        )