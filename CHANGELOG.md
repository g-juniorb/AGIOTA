# Changelog

Este arquivo registra as funcionalidades presentes na versão atual do GIGI Cobrador. A interface identifica a versão como **1.0.0**.

## [1.0.0] - Estado atual

### Adicionado

- Aplicativo desktop para preparar cobranças de aceite com interface PySide6.
- Leitura de planilhas Excel com seleção de linhas por indicador `S`, link do grupo e link das demandas.
- Personalização da mensagem por modelo, incluindo saudação por horário, link das demandas e menção ao gerente.
- Conexão ao Microsoft Teams por perfil persistente em Chrome ou Edge.
- Modo assistido para acompanhar a automação no navegador.
- Tabela de cobranças com status, progresso, contadores e log da execução.
- Repetição de tentativas com intervalo e tratamento de falha de acesso ao grupo.
- Reexecução das cobranças que falharam.
- Exportação de evidências em arquivos de log, resultado Excel e resumo.
- Relatório Excel separado para cobranças com erro.
- Preferência de navegador, persistida localmente, e cópia do modelo Excel incluído.
