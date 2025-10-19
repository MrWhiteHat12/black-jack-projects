import random
import sys
import time
import builtins
import card_lib

# Override print to slow print everything
original_print = builtins.print


def slow_print(*args, delay=0.05, **kwargs):
    text = " ".join(str(arg) for arg in args)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write('\n')
    sys.stdout.flush()


builtins.print = slow_print  # override the print function
total_cards = card_lib.all_cards.copy()  # deck to draw from

shown_computer_cards = ["?"]
computer_cards = [0]
player_cards = []
player_total = [0]
computer_total = [0]
ending = False
playing = False
players_funds = 500
pot = 0


animation = (".-------. .-------. .-------. .-------. .-------.\n"
             "| A ♠   | |10 ♦   | | 1 ♣   | |10 ♥   | | A ♣   |\n"
             "|       | |       | |       | |       | |       |\n"
             "|   ♠   | |  ♦♦♦  | |   ♣   | |  ♥♥♥  | |   ♣   |\n"
             "|       | |       | |       | |       | |       |\n"
             "|   ♠ A | |   10  | |   1   | |   10  | |   ♣ A |\n"
             "'-------' '-------' '-------' '-------' '-------'")


def give_card(goes_to: list, goes_to_total: list):
    choice = random.choice(total_cards)
    total_cards.remove(choice)  # remove card from deck
    goes_to.append(choice)      # add card string to hand
    # add card value to total
    goes_to_total[0] += card_lib.get_card_value(choice)


original_print(animation)
print("Do you want to play Black Jack (y/n): ", end='')
want_to_play = input().lower()
if want_to_play == "y":
    while want_to_play == "y":
        # eh
        playing = True
        shown_computer_cards = ["?"]
        computer_cards = [0]
        player_cards = []
        player_total = [0]
        computer_total = [0]
        pot = 0

        # Computer initial deal
        give_card(shown_computer_cards, computer_total)
        computer_cards = shown_computer_cards.copy()
        computer_cards.remove("?")
        give_card(computer_cards, computer_total)

        # Player initial deal
        for i in range(2):
            give_card(player_cards, player_total)

        print(f"dealers cards {shown_computer_cards}\n\n")

        # Game loop
        while playing and not ending:
            print(player_cards)
            print(f"your total is {player_total[0]}")
            print("Do you want to hit(1) or stand(2): ", end='')
            action = input()
            print(f"you have ", players_funds)
            print("how much do you want to bet? ")
            pot = int(input())

            if action == '1':  # hit
                give_card(player_cards, player_total)
            elif action == '2':  # stand
                ending = True
                playing = False
            else:
                print("Invalid input, please enter 1 or 2.")

            # check for bust
            if player_total[0] > 21:
                ending = True
                playing = False

        # Game end logic
        if ending:
            if player_total[0] > 21:
                print(
                    f"your new hand was {player_cards} with a total of {player_total[0]}")
                print(f"the dealer had {computer_cards}")
                print("you bust")
                players_funds -= pot
                print(players_funds)
            elif player_total[0] > computer_total[0]:
                print(f"the dealer had {computer_cards}")
                print("you win")
                players_funds += pot
                print(players_funds)
            elif player_total[0] < computer_total[0]:
                print(f"the dealer had {computer_cards}")
                print("you lose")
                players_funds -= pot
                print(players_funds)
            else:
                print("tie")

        print("do you want to play again? (y,n)")
        want_to_play = input()

elif want_to_play == "♣♣♣♣":
    print("developer mode == True")
    print("which would matter if OB had coded a developer mode")

else:
    print("Maybe next time!")
