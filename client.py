import socket
import threading
import json

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345


def d(data):
    return json.dumps(data).encode('utf-8')


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            try:
                message = json.loads(data.decode())
            except json.JSONDecodeError:
                print(data.decode())
            else:
                if "command" in message:
                    cmd = message.get("command")
                    if cmd == "name_request":
                        name = input("Choose your name: ")
                        sock.sendall(d({"command": "name_send", "data": name}))
                    elif cmd == "message":
                        print(message.get("data"))
                    elif cmd == "initial_hand":
                        data_body = message.get("data", {})
                        hand = data_body.get("hand")
                        total = data_body.get("total")
                        print(f"Initial hand received: {hand} total: {total}")
                    else:
                        print(f"[DEBUG] Unknown message: {message}")
                else:
                    print(f"[DEBUG] {message}")
        except ConnectionResetError:
            print("Connection closed by server.")
            break


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
    except ConnectionRefusedError:
        print(
            f"Unable to connect to server {SERVER_IP}:{SERVER_PORT}. Is the server running?")
        return
    except Exception as e:
        print(f"Connection error: {e}")
        return
    print(f"Connected to server {SERVER_IP}:{SERVER_PORT}")
    # Start receiver in a background thread so we can send from stdin as well
    recv_thread = threading.Thread(
        target=receive_messages, args=(client_socket,), daemon=True)
    recv_thread.start()

    try:
        while True:
            msg = input()
            if msg.lower() in ("quit", "exit"):
                break
            # send as a JSON message using the same format server expects
            try:
                client_socket.sendall(d({"command": "message", "data": msg}))
            except BrokenPipeError:
                print("Connection lost.")
                break
    except KeyboardInterrupt:
        pass
    finally:
        client_socket.close()
        print("Disconnected from server.")


if __name__ == "__main__":
    start_client()
