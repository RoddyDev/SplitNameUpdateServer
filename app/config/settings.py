# Primeiramente você deverá criar um token OAuth para conseguir se autenticar com a API da Twitch
# Link para autenticação:
# https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=owa12694zio5ifwd22vnfv3udkj00g&redirect_uri=https://auth.roddydev.com/register_oauth&scope=channel%3Aread%3Aredemptions+channel%3Amanage%3Aredemptions

# Este é o ID do aplicativo que irá se autenticar. Por favor não mudar.
eventsub_client_id = "owa12694zio5ifwd22vnfv3udkj00g"

# Este é o ID do seu canal. Não é informação privada.
broadcaster_id = ""

# Este é a sua chave de autenticação para a API da Twitch. Isso é informação privada e não deve ser compartilhada.
eventsub_oauth = ""

# Constants das rewards que será enviada para o plugin do LiveSplit. Não mudar, a não ser que você saiba o que está fazendo e quer modificar o plugin do LiveSplit, ou adicionar novas features.
SPLIT_FIRST = 0
SPLIT_LAST = 1
SPLIT_RANDOM = 2
SPLIT_CURRENT = 3

# Reward ID codes

# Deve ser configurado depois de preencher sua broadcaster_id e chave OAuth. Inicie o aplicativo no modo debug (debug.bat), e espere autenticar.
# Depois de conectado e autenticado, comece a enviar as rewards desejadas pelo seu canal. Será loggado como "[Nome da reward] -> [Código da reward]"
# Você irá querer pegar o código da reward, e inserir junto com uma das constants desejadas, respeitando a sintaxe codes = [(code, const), (code, const)]
# Você poderá adicionar várias rewards para o mesmo objetivo, na ordem que quiser.
# Códigos errados não irão mandar um erro, somente serão ignorados.

# Exemplo:
# codes = [
#     ("8df69b47-bb09-4e60-b2a7-a7868d840f90", SPLIT_FIRST), 
#     ("69ea097c-afc7-86f5-4d96-cef67878a60e", SPLIT_LAST),
#     ("3dea90df-38a9-44ba-86f5-504b04a71f9a", SPLIT_LAST), 
#     ("69ea097c-7140-4d96-9079-61b44063d78f", SPLIT_RANDOM), 
#     ("7ed874b5-cb9a-4579-afc7-cef67878a60e", SPLIT_CURRENT)
# ]

codes = []
