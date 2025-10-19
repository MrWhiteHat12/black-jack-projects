# server.py
import socket
import threading
import json
import multiplayer
import blackJackPlayer
import singlePlayer

player_setup = False
HOST = '127.0.0.1'
PORT = 12345         # port to bind on

connected_players = []   # list of PlayerConnection objects (by name)
numbered_players = []    # list of PlayerConnection objects (by number)
number_joined = 1
# map PlayerConnection.id -> blackJackPlayer.player instance
server_players = {}


def d(data):
    return json.dumps(data).encode('utf-8')


class PlayerConnection:
    def __init__(self, connection, id, num):
        self.connection = connection
        self.id = id
        self.name = 'Unknown'
        self.num = num
        self.player = None
        self.connection.sendall(d({"command": "name_request"}))

    def handle(self, data):
        if data.get('command') == 'name_send':
            self.name = data.get('data')
            print(f"[+] Player connected: {self.name} (#{self.num})")
            # create a server-side player object and deal an initial hand
            try:
                # default starting funds - adjust as needed
                starting_funds = 100
                p = blackJackPlayer.player(ip=self.name, funds=starting_funds, hand=[], total=[
                                           0], playing=True, in_for=0, ace_high=True, host=False)
                # deal initial two cards
                try:
                    p.give_player_hand()
                except Exception:
                    # fallback: try using singlePlayer directly
                    try:
                        singlePlayer.give_card(p.hand, p.total)
                        singlePlayer.give_card(p.hand, p.total)
                    except Exception:
                        pass
                self.player = p
                server_players[self.id] = p
                # send the initial hand to the client
                try:
                    self.connection.sendall(
                        d({"command": "initial_hand", "data": {"hand": p.hand, "total": p.total}}))
                except Exception:
                    pass
            except Exception as e:
                print(f"[!] Error creating player for {self.name}: {e}")
        elif data.get('command') == 'message':
            print(f"{self.name}: {data.get('data')}")


def broadcast(message):
    # message should be bytes; helper d() exists to encode dicts to JSON bytes
    for connection_object in connected_players:
        try:
            connection_object.connection.sendall(message)
        except Exception:
            try:
                connection_object.connection.close()
            except Exception:
                pass
            if connection_object in connected_players:
                connected_players.remove(connection_object)


def targeted_message_name(message, target_name):
    for player in connected_players:
        if player.name == target_name:
            try:
                player.connection.sendall(
                    d({"command": "message", "data": message}))
                print(f"Sent message to {player.name}: {message}")
            except:
                player.connection.close()
                connected_players.remove(player)
            break
    else:
        print(f"Player '{target_name}' not found.")


def targeted_message_num(message, target_num):
    for player in numbered_players:
        if str(player.num) == str(target_num):  # make sure it works even if user types string
            try:
                player.connection.sendall(
                    d({"command": "message", "data": message}))
                print(f"Sent message to player #{player.num}: {message}")
            except:
                player.connection.close()
                numbered_players.remove(player)
            break
    else:
        print(f"Player number {target_num} not found.")


def handle_client(client_socket, addr):
    global number_joined
    print(f"[+] New connection from {addr}")
    connection_object = PlayerConnection(
        connection=client_socket, id=len(connected_players), num=number_joined
    )
    connected_players.append(connection_object)
    numbered_players.append(connection_object)
    number_joined += 1

    try:
        while True:
            data = connection_object.connection.recv(1024)
            if not data:
                break
            connection_object.handle(json.loads(data.decode()))
    except ConnectionResetError:
        print(f"[!] Connection lost: {addr}")
    finally:
        print(f"[-] Client {addr} disconnected")
        if connection_object in connected_players:
            connected_players.remove(connection_object)
        if connection_object in numbered_players:
            numbered_players.remove(connection_object)
        connection_object.connection.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[✓] Server listening on {HOST}:{PORT}")

    # Thread for server input (optional)
    threading.Thread(target=server_input, daemon=True).start()

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(
            client_socket, addr), daemon=True).start()


def server_input():
    while True:
        msg = input()
        if msg.startswith("@"):  # message to specific player by NAME
            parts = msg.split(" ", 2)
            if len(parts) >= 3:
                target_name = parts[1]
                message = parts[2]
                targeted_message_name(message, target_name)
            else:
                print("Usage: @ name message")

        elif msg.startswith("/"):  # message to specific player by NUMBER
            parts = msg.split(" ", 2)
            if len(parts) >= 3:
                target_num = parts[1]
                message = parts[2]
                targeted_message_num(message, target_num)
            else:
                print("Usage: / number message")

        else:
            # broadcast message to everyone
            broadcast(d({"command": "message", "data": msg}))


if __name__ == "__main__":
    start_server()
