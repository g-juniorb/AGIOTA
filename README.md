# GIGI Cobrador

Aplicativo desktop para preparar cobranças de aceite no Microsoft Teams a partir de uma planilha Excel. O sistema carrega grupos e mensagens, permite revisar os dados e automatiza a abertura dos grupos e a composição das mensagens com menção ao gerente.


## Funcionalidades

- Interface desktop construída com PySide6.
- Carregamento e pré-visualização de cobranças em arquivos `.xlsx`.
- Uso de modelo de mensagem com saudação automática, link das demandas e menção ao gerente.
- Abertura de grupos do Teams usando o navegador instalado e um perfil persistente.
- Modo assistido, com o navegador visível durante a automação.
- Acompanhamento de progresso, status por cobrança e registro de atividade.
- Até três tentativas para operações com erro, com intervalo de cinco segundos entre tentativas.
- Reexecução das cobranças que falharam.
- Exportação de evidências com log, planilha de resultados e resumo da execução.
- Geração de relatório Excel com os erros.
- Preferência de navegador (automático, Chrome ou Edge) e opção para baixar o modelo.

## Requisitos

- Python instalado.
- Google Chrome ou Microsoft Edge instalado.
- Acesso à conta do Microsoft Teams que participa dos grupos usados na planilha.

As dependências Python estão listadas em [`requirements.txt`](./requirements.txt): Playwright, openpyxl, pandas, PySide6 e PyInstaller.

## Instalação e execução

1. Clone o repositório e entre na pasta do projeto.
2. Crie e ative um ambiente virtual, se desejar.
3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicie o aplicativo:

   ```bash
   python main.py
   ```

Na primeira execução, use **Conectar ao Teams** para entrar na conta. O perfil do navegador é mantido entre execuções. Em **Configurações**, selecione automático, Chrome ou Edge. O aplicativo localiza Chrome e Edge nos caminhos padrão do Windows e macOS; em outros sistemas, a localização automática não está implementada.

## Formato da planilha

O botão **Baixar Modelo** salva uma cópia do modelo incluído no aplicativo. A planilha de entrada precisa ter:

1. **Primeira aba — dados das cobranças:** a partir da linha 2, use a coluna A para indicar se a cobrança será processada (`S`), a coluna B para o nome do grupo (com hiperlink para o grupo do Teams) e a coluna C para o link das demandas.
2. **Segunda aba — mensagem:** a célula A1 contém o texto-modelo da mensagem.

No texto-modelo, use:

- `#Saudacao` para inserir “Bom dia”, “Boa tarde” ou “Boa noite”, conforme o horário.
- `#LinkDemandas` para inserir o conteúdo da coluna C.
- `#Gerente` no ponto em que a menção ao gerente deve aparecer.

Somente as linhas marcadas com `S` na coluna A são carregadas. Confira os grupos, links, nomes e texto na tabela do aplicativo antes de iniciar.

## Como usar

1. Conecte-se ao Teams.
2. Selecione a planilha `.xlsx` preenchida conforme o modelo.
3. Revise as cobranças e mensagens exibidas.
4. Opcionalmente, ative **Modo Assistido** para visualizar o navegador.
5. Inicie a execução e acompanhe os status e o log.
6. Revise no Teams se as mensagens foram efetivamente enviadas. No estado atual, o envio automático está desativado.
7. Se necessário, reexecute as falhas ou exporte as evidências.

## Arquivos gerados e dados locais

O aplicativo armazena configuração, perfil persistente do navegador, relatórios e logs na pasta de dados do usuário:

- Windows: `%LOCALAPPDATA%/GIGI`
- macOS: `~/Library/Application Support/GIGI`
- Outros sistemas: `~/.GIGI`

O relatório de erros é salvo como `reports/erros.xlsx`. A opção **Exportar Evidências** cria uma pasta com data e hora contendo `Log_Execucao.txt`, `Planilha_Resultado.xlsx` e `Resumo.txt`.

## Estrutura do projeto

- `main.py`: inicialização da aplicação.
- `gui/`: janela principal, configurações e recursos visuais.
- `models/`: modelo de dados da cobrança.
- `pages/`: interação com as páginas do Teams.
- `services/`: leitura da planilha, automação do Teams e relatórios.
- `workers/`: execução do processamento em thread separada.
- `utils/`: caminhos, navegador, configurações e saudação.
- `exceptions/`: exceções específicas do Teams.

## Changelog

Consulte [`CHANGELOG.md`](./CHANGELOG.md) para ver o registro das funcionalidades e limitações documentadas.
