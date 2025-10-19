import card_lib
import random
import sys
import time
import builtins
import blackJackPlayer
import singlePlayer
from blackJackPlayer import player
import multiplayer
import server
import client

print('how many people are playing:')
num_player = input()
print('what is the starting funds of each player:')
funds = input()
print('have you played before (y/n)')
played = input()


if int(num_player) > 1:
    multiplayer.multiplayer(num_player)

elif num_player == 1:
    singlePlayer.singlePlayer(funds)