import card_lib
import random
import sys
import time
import builtins
import blackJackPlayer
import singlePlayer
from blackJackPlayer import player
import server
import client


print("Are you the game host? (y/n)")
is_host = input().strip().lower() == "y"

# Ask number of players and starting funds
num_players = 1
starting_funds = 100
try:
    num_players = int(
        input("How many players (including host/client)? ").strip())
except Exception:
    print("Invalid number, defaulting to 1")

try:
    starting_funds = int(input("Starting funds for each player? ").strip())
except Exception:
    print("Invalid funds, defaulting to 100")

# If this machine is the host, start the server in a background thread so we can
# continue to create player objects locally.
if is_host:
    import threading


    threading.Thread(target=server.start_server, daemon=False).start()
    print("Server started in background thread.")


    host_player = player(ip="host", funds=starting_funds, hand=[], total=[
                         0], playing=True, in_for=0, ace_high=True, host=True)
    try:
        host_player.give_player_hand()
    except Exception:
        pass

    print(
        f"Host player created: {host_player.ip} hand: {host_player.hand} total: {host_player.total}")

    # Wait for remote clients to join. We assume `num_players` includes the host.
    expected_remote = max(0, num_players - 1)
    print(f"Waiting for {expected_remote} remote player(s) to join...")
    import time
    try:
        while True:
            try:
                remote_count = len(server.server_players)
            except Exception:
                remote_count = 0
            if remote_count >= expected_remote:
                break
            print(f"Waiting... {remote_count}/{expected_remote} joined")
            time.sleep(1)

        # Gather all hands: host + server-side players
        all_players = [host_player]
        try:
            all_players.extend(list(server.server_players.values()))
        except Exception:
            pass

        print("All players have joined. Hands:")
        for p in all_players:
            print(f"{p.ip} hand: {p.hand} total: {p.total}")


        print("Server is running. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down host application.")
    except KeyboardInterrupt:
        print("Interrupted while waiting for players.")
else:
    # If not host, start client which will connect to the host server
    client.start_client()
