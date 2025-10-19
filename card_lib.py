all_cards = [
    "A♠", "2♠", "3♠", "4♠", "5♠", "6♠", "7♠", "8♠", "9♠", "10♠", "J♠", "Q♠", "K♠",
    "A♥", "2♥", "3♥", "4♥", "5♥", "6♥", "7♥", "8♥", "9♥", "10♥", "J♥", "Q♥", "K♥",
    "A♦", "2♦", "3♦", "4♦", "5♦", "6♦", "7♦", "8♦", "9♦", "10♦", "J♦", "Q♦", "K♦",
    "A♣", "2♣", "3♣", "4♣", "5♣", "6♣", "7♣", "8♣", "9♣", "10♣", "J♣", "Q♣", "K♣"
]


def get_card_value(card):
    # Return Blackjack numeric value for a given card string.
    rank = card[:-1]  # Remove suit character
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11
    else:
        return int(rank)


def get_card_value_13(card):
    # Return Blackjack numeric value for a given card string.
    rank = card[:-1]  # Remove suit character
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11
    elif rank == 2:
        return 299
    else:
        return int(rank)
