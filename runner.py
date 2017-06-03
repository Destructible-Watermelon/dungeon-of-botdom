from base import BasePlayer


class RunAway(BasePlayer):

    def __init__(self):
        self.cards = 13

    def start_turn(self, last_turn):
        if last_turn is not None:
            self.cards -= 1  # opponents play
        if self.cards < 4:
            return 0 * last_turn  # avoid the ---noid--- squiggles
        else:
            return 1

    def play(self, card):
        if self.cards > 11: # if it is the first turn
            choice = 5  # remove armour
        else:
            choice = 6  # put the card in the dungeon
        self.cards -= 1  # this play
        return choice

    def vorpal_choice(self, last_turn):
        return 5  # without using more memory, this is the best choice statistically

    def result(self, bot, result):
        self.cards = 13
