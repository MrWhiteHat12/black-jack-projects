import card_lib
import random
import sys
import time
import builtins
import blackJackPlayer
import singlePlayer
from blackJackPlayer import player


def betting_proccess(raise_bet: bool, call_bet: bool, player_obj, bet_to_play, pot):
    if call_bet:
        if bet_to_play < player_obj.funds:
            player_obj.funds -= bet_to_play - player_obj.in_for
            pot += bet_to_play - player_obj.in_for
            player_obj.in_for = bet_to_play
        else:
            player_obj.in_for = player_obj.in_for + player_obj.funds
            pot += player_obj.funds
            player_obj.funds = 0

    if raise_bet:
        print(
            f"How much should the new bet be? Current bet: {bet_to_play}. "
            f"Max you can raise to: {player_obj.in_for + player_obj.funds}"
        )
        new_bet = int(input())
        pot += new_bet - player_obj.in_for
        player_obj.funds -= new_bet - player_obj.in_for
        player_obj.in_for = new_bet
        bet_to_play = new_bet

    return bet_to_play, pot


def check_for_aces(player_):
    """Adjust Aces from 11 to 1 if total exceeds 21."""
    if player_.playing:
        # Handle both list and int total types
        if isinstance(player_.total, list):
            total_val = player_.total[0]
        else:
            total_val = player_.total

        # Only adjust if bust
        if total_val > 21:
            for card in player_.hand:
                if 'A' in card and total_val > 21:
                    total_val -= 10  # downgrade one Ace from 11 to 1

        # Update player's total
        if isinstance(player_.total, list):
            player_.total[0] = total_val
        else:
            player_.total = total_val


def multiplayer(num_of_players, funds, list_of_players):
    total_cards = card_lib.all_cards.copy()
    players = []
    bet_to_play = 2
    pot = 0

    for i in len(list_of_players):
        p = player(ip=f"Player_{i}", funds=funds, hand=[], total=[
                   0], playing=True, in_for=0, ace_high=True)
        p.give_player_hand()
        check_for_aces(p)
        players.append(p)
        print(f"Here is your hand: {p.hand}, total: {p.total}")

        option = input(f"Call(1) for {bet_to_play}, Raise(2), or Fold(3)? ")
        if option == "1":
            bet_to_play, pot = betting_proccess(
                False, True, p, bet_to_play, pot)
        elif option == "2":
            bet_to_play, pot = betting_proccess(
                True, False, p, bet_to_play, pot)
        elif option == "3":
            p.playing = False
            p.hand.clear()
        else:
            print("Invalid input")

    for i in len(list_of_players):
        if players[i].playing:
            print(
                f"Here is your hand: {players[i].hand}, total: {players[i].total}")
            while True:
                action = input("Hit(1) or Stand(2)? ")
                if action == "1":
                    singlePlayer.give_card(players[i].hand, players[i].total)
                    check_for_aces(players[i])
                    print(
                        f'your new hand is: {players[i].hand}   your new total is: {players[i].total}')
                elif action == "2":
                    break
                else:
                    print("Invalid input")

    for i in len(list_of_players):
        if players[i].playing:
            if players[i].in_for == bet_to_play:
                action = input("Do you want to raise (y/n)? ").lower()
                if action == "y":
                    bet_to_play, pot = betting_proccess(
                        True, False, players[i], bet_to_play, pot)
            elif players[i].in_for < bet_to_play:
                action = input(
                    f"You’re in for {players[i].in_for}. Call(1) to {bet_to_play}, "
                    "Raise(2), or Fold(3)? "
                )
                if action == "1":
                    bet_to_play, pot = betting_proccess(
                        False, True, players[i], bet_to_play, pot)
                elif action == "2":
                    new_bet = int(input("Enter new total bet: "))
                    pot += new_bet - players[i].in_for
                    players[i].funds -= new_bet - players[i].in_for
                    players[i].in_for = new_bet
                    bet_to_play = new_bet
                elif action == "3":
                    players[i].hand.clear()
                    players[i].playing = False

    # Show remaining hands
    for p in players:
        if p.playing:
            print(f"{p.ip} final hand: {p.hand}, total: {p.total}")

    # Determine winner
    winner = None
    best_distance = 100

    for p in players:
        if p.playing:
            my_distance = 21 - p.total[0]  # Assuming total[0] is main total
            if 0 <= my_distance < best_distance:
                best_distance = my_distance
                winner = p

    if winner:
        print(f"The winner is {winner.ip}!")
        winner.funds += pot
    else:
        print("No winner.")

    pot = 0
    for p in players:
        p.hand.clear()
        p.in_for = 0


if __name__ == "__main__":
    multiplayer(2, 200, )
