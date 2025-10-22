# SaldoRescisorioFGTS
Automação de busca de saldos rescisórios do FGTS no site Conectividade da CAIXA


Requisitos do processo: Números de PIS e certificado digital da empresa.

Design Patterns: Modularizei o código de forma a garantir fácil entendimento do propósito de cada módulo e facilitando o uso das funções em demais desenvolvimentos.
De momento a automação recebe dados de um Excel para não afetar a consistência do banco de dados, porém assim que as inconsistências do site conectividade estiverem mapeadas e resolvidas, leitura passará ao banco de dados.
 
Requisitos do robô: Playwright, Pandas, pasta com caminho para armazenamento do contexto persistente do playwright.Firefox.
 
Módulos
Main.py: Estrutura principal que recebe a planilha e inicia o robô.
Libs.py: Como utilizei diversas vezes as mesmas bibliotecas, coloquei em um arquivo separado que é importado em todos os módulos.
Utils.py: funções genéricas que podem ser chamadas a qualquer momento durante a execução e utilizadas em loops.
Ler_planilha.py: Possui funções referentes ao inicio e encerramento do processo, lendo a planilha, identificando os itens que não foram atualizados recentemente ou itens com erro na última execução, inicia o Playwright e no fim de cada passo do loop salva uma planilha temporária que substitui a planilha principal (para evitar inconsistência no salvamento em caso da aplicação quebrar nas inconsistências do site da Caixa).
Conectividade.py: Módulo que executa o processo em si, acessando o site https://conectividadesocialv2.caixa.gov.br/sicns/ com o certificado digital que está no contexto persistente do Firefox, e caso não possua contexto persistente cria um a partir do caminho os.path.expanduser(rf'~\Desktop\fgts\persistente') (se pastas não existirem, será necessário criar as mesmas, ou apontar na linha 6 o novo caminho do contexto persistente), e busca pelo saldo rescisório do FGTS a partir do número do PIS.

Execução
Para execução do robô são necessários:
•	Certificado da empresa instalado na máquina (A1)
•	Dados de números de PIS a serem pesquisados
A execução está sendo realizada diretamente na IDE, sendo assim, basta instalar os requirements.txt e executar o arquivo main.py 
