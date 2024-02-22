# LiveSplit split name update server
# Written by Roddy
# Last update: February 22, 2024

import asyncio
import websockets
import requests
import json
import sys
import config.settings as o_keys

codes = o_keys.codes

connected_clients = set()

async def eventsub(debug_mode=False):
    while True:
        print("Conectando ao Twitch EventSub")
        async with websockets.connect("wss://eventsub.wss.twitch.tv/ws") as socket:
            try:
                # Conectado. Esperar por session_welcome
                print("Esperando por session_welcome")
                msg = await socket.recv()
                data = json.loads(msg)
                try:
                    if (data["metadata"]["message_type"] == "session_welcome"):
                        session_id = data["payload"]["session"]["id"]
                        print(f"Recebido session_welcome (Session ID: {session_id}).")
                        sub = await subscribe_event(session_id)
                        if (sub == 202):
                            print("Sucesso ao inscrever ao evento.")
                        else:
                            print("Falha ao inscrever ao evento. Fechando socket...\n")
                            print("Favor gerar um novo código OAuth nesse link:")
                            print("https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=owa12694zio5ifwd22vnfv3udkj00g&redirect_uri=https://auth.roddydev.com/register_oauth&scope=channel%3Aread%3Aredemptions+channel%3Amanage%3Aredemptions")

                            # Fechar todos os subprocessos ativos
                            if asyncio.get_event_loop().is_running():
                                for task in asyncio.all_tasks():
                                    try:
                                        task.cancel()
                                    except Exception as ex:
                                        pass
                except:
                    print("Ocorreu um erro ao tentar conectar ao Twitch EventSub")
                    # Fechar todos os subprocessos ativos
                    if asyncio.get_event_loop().is_running():
                        for task in asyncio.all_tasks():
                            try:
                                task.cancel()
                            except Exception as ex:
                                pass

                if (debug_mode == True):
                    print("DEBUG MODE")

                while True:
                    msg = await socket.recv()
                    data = json.loads(msg)
                    
                    # Only get redemptions
                    match (data["metadata"]["message_type"]):
                        case "notification":
                            if (debug_mode == False):
                                event = data["payload"]["event"]
                                for _i in codes:
                                    if (_i[0] == event["reward"]["id"]):
                                        print(f'{event["user_name"]}: {event["reward"]["title"]} -> {event["user_input"]}')
                                        response = {
                                            "type": _i[1],
                                            "split_name": event["user_input"]
                                        }

                                        asyncio.create_task(broadcast(json.dumps(response)))
                            else:
                                event = data["payload"]["event"]
                                print(f"{event["reward"]["title"]} -> {event["reward"]["id"]}")
                        case "session_reconnect":
                            url = data["payload"]["session"]["reconnect_url"]
                            print(f"Para fazer: Implementar session_reconnect para não ter o risco de perder notificações! {url}")
                            print("Mas por agora, fechando a conexão e reconectando...")
                            await socket.close()

                        case _:
                            pass
            except websockets.exceptions.ConnectionClosedOK as ex:
                print(f"Conexão encerrada. {ex}")
            except websockets.exceptions.ConnectionClosedError as ex:
                print(f"Conexão encerrada com um erro: {ex}")
            except KeyError as err:
                print(f"Erro com mensagem: {msg}")
            except KeyboardInterrupt:
                print("Fechando aplicativo...")
                await socket.close()
                # Fechar todos os subprocessos ativos
                if asyncio.get_event_loop().is_running():
                    for task in asyncio.all_tasks():
                        try:
                            task.cancel()
                        except Exception as ex:
                            pass


async def subscribe_event(s_id):
    print(f"Tentando se inscrever ao evento \"channel.channel_points_custom_reward_redemption.add\" com session ID {s_id}")
    request = {
        "type": "channel.channel_points_custom_reward_redemption.add", 
        "version": "1",
        "condition": {"broadcaster_user_id": o_keys.broadcaster_id},
        "transport": {"method": "websocket", "session_id": s_id}
    }

    header_list = {
        'Authorization': f'Bearer {o_keys.eventsub_oauth}',
        'Client-Id': f'{o_keys.eventsub_client_id}',
        'Content-Type': 'application/json'
    }

    poop = requests.post('https://api.twitch.tv/helix/eventsub/subscriptions', headers=header_list, data=json.dumps(request))
    if (poop.status_code != 202):
        print(poop.text)

    return poop.status_code

async def handle_user_request(socket):
    # Adicionar a lista de clientes conectados
    connected_clients.add(socket)
    ip = f"[{socket.remote_address[0]}]:{socket.remote_address[1]}"
    print(f"Cliente LiveSplit com endereço {ip} conectado.")

    try:
        # O cliente não precisar enviar nada, então entre em um loop infinito
        while True:
            msg = await socket.recv()
    except:
        print(f"{ip} disconectado.")
        connected_clients.remove(socket)

# Enviar dados ao cliente
async def send_message(ws, message):
    try:
        await ws.send(message)
    except:
        connected_clients.remove(ws)

# Enviar dados a todos os clientes conectados
async def broadcast(message):
    for client in connected_clients:
        asyncio.create_task(send_message(client, message))

async def main(arg):
    if (arg.lower() == "debug"):
        try:
            task = asyncio.create_task(eventsub(True))
            await task
        except:
            pass
    else: 
        # Conectar ao Twitch EventSub
        try:
            async with websockets.serve(handle_user_request, "::1", 61000):
                print("Servidor WebSocket iniciado no endereço [::1] na porta 61000")
                main_task = asyncio.create_task(eventsub(False))
                await main_task
        except:
            pass
        

if __name__ == "__main__":
    print("helpme")
    try:
        try:
            main = asyncio.run(main(sys.argv[1]))
        except IndexError:
            asyncio.run(main(""))
    except KeyboardInterrupt:
        pass