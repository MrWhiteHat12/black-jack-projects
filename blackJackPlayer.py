import socket
import threading
import singlePlayer


class player:
    def __init__(self, ip: str, funds: int, hand: list, total: list, playing: bool, in_for: int, ace_high: bool, host: bool):
        self.funds = funds
        self.ip = ip
        self.hand = hand
        self.total = total
        self.playing = playing
        self.in_for = in_for
        self.host = host

    def give_player_hand(self):
        singlePlayer.give_card(self.hand, self.total)
        singlePlayer.give_card(self.hand, self.total)

    def give_card(self):
        singlePlayer.give_card(self.hand, self.total)
