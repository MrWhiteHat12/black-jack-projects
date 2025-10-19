import card_lib
import random
import sys
import time
import builtins
import card_lib
import blackJackPlayer
import singlePlayer
from blackJackPlayer import player


def betting_proccess(raise_bet: bool, call_bet: bool, player: list[player]):
    if call_bet == True:
        if bet_to_play < player.funds:
            player.funds -= bet_to_play - player.in_for
            pot += bet_to_play - player.in_for
            player.in_for = bet_to_play
        else:
            player.in_for = player.in_for + player.funds
            pot += player.funds
            player.funds = 0
    if raise_bet == True:
        print(
            f'how much should the new bet to play current bet to play is {bet_to_play} the max you can raise to is {player.in_for + player.funds}')
        bet_to_play = input()
        pot += bet_to_play - player.in_for
        player.funds -= bet_to_play - player.in_for
        player.in_for = bet_to_play

def multiplayer(num_of_players):
    players_num = num_of_players
    total_cards = card_lib.all_cards.copy()
    player_hands = {}
    player_totals = {}
    players = []
    bet_to_play = 2
    pot = 0


    players: list[player] = []
    for i in range(players_num):
        p = player(ip=f"Player_{i}", funds=499, hand=[],
                total=[0], playing=True, in_for=0)
        p.give_player_hand()
        players.append(p)
        print(f"Here is your hand: {p.hand} giving a current total of {p.total}")

        option = int(input(
            f"do you want to call(1) for {bet_to_play}, raise(2) (input the total you want to put in), or fold(3)"))
        if option == 1:
            betting_proccess(False, True,players[i])
        elif option == 2:
            betting_proccess(True, False,players[i])
        elif option == 3:
            p.playing = False
            p.hand.clear()
        else:
            print("invalid input")

    print(players[1].hand)

    for i in range(players_num):
        if players[i].playing == True:
            print("do you want to hit(1) or stand(2)?")
            action = input()
            if action == 1:
                while action == 1:
                    singlePlayer.give_card(players[i].hand, players[i].total)
                    print(players[i].hand)
                    print("do you want to hit(1) or stand(2)?")
                    action = input()
        else:
            players[i].hand.clear()
            players[i].playing = False

    for i in range(players_num):
        if players[i].playing == True:
            if players[i].in_for == bet_to_play:
                print("do you want to raise (y/n)")
                action = input()
                if action == "n":
                    pass
                if action == "y":
                    betting_proccess(True,False,players[i])

                else:
                    print('invalid input')
            if players[i].in_for < bet_to_play:
                print(
                    f'you are currently in for {players[i].in_for} do you want to call for a total of {bet_to_play}(1) reraise(2) or fold(3)')
                action = input()
                if action == 1:
                    betting_proccess(False,True,players[i])

                elif action == 2:
                    print(
                        f'the current bet to play is {bet_to_play} give a greater bet that is what your raising to.')
                    bet_to_play == input()
                    pot += bet_to_play-players[i].in_for
                    players[i].funds -= bet_to_play-players[i].in_for
                    players[i].in_for += bet_to_play-players[i].in_for

                elif action == 3:
                    players[i].hand.clear()
                    players[i].playing = False
                else:
                    print("error")


    for i in range(players_num):
        if players[i].in_for < bet_to_play:
            print(
                f'the current bet to play is {bet_to_play} would you like to call(1) or fold(2)')
            action = input()
            if not action == 1 or action == 2:
                action = 2
            if action == 1:
                pot += bet_to_play-players[i].in_for
                players[i].funds -= bet_to_play-players[i].in_for
                players[i].in_for += bet_to_play-players[i].in_for
            if action == 2:
                players[i].hand.clear()
                players[i].playing = False


    for i in player:
        if players[i].playing == True:
            print(players[i].hand)
