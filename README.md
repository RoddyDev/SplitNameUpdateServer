# SplitNameUpdate
Esse é o servidor local para usar com o plugin de LiveSplit para automaticamente atualizar o nome das splits através das recompensas do seu canal da Twitch.

## Como usar:
1. Instalar Python 3, download aqui: https://www.python.org/downloads/
2. Durante a instalação, tenha certeza que esteja instalando o pip.
3. Baixe o aplicativo aqui: https://github.com/RoddyDev/SplitNameUpdate/releases
4. Depois de ter instalado o Python, vá até a pasta do projeto, e rode o arquivo `install_requirements.bat`, isso irá instalar os pacotes necessários para que o aplicativo funcione.
5. Abra o arquivo de configurações em `app/config/settings.py` em um editor de texto, e siga as instruções.
6. Depois de tudo preenchido, abra o arquivo `debug.bat`, use o para configurar as recompensas usadas para mudar os splits.
7. Depois de tudo configurado, copie os arquivos da pasta LiveSplit para a pasta Components da sua instalação do LiveSplit.
8. Rode o arquivo `start.bat` daqui em diante. Isso irá criar um servidor para que consiga conectar o LiveSplit.

# Planos
1. Ter mais controle de configurações tanto no servidor quanto no plugin de LiveSplit
2. Dominar completamente como funciona o asyncio e C#
3. Criar uma GUI para fazer do aplicativo um executável ao invés de algo que precise ser executado em um console.
