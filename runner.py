from base import BasePlayer


class RunAway(BasePlayer):

    def __init__(self):
        self.cards = 13
        self.armoured = True

    def start_turn(self, last_turn):
        if last_turn is not None:
            self.cards -= 1  # opponents play
        if last_turn is 5:
            self.armoured = False

        if self.cards < 4:
            return 0 * last_turn  # avoid the ---noid--- squiggles
        else:
            return 1

    def play(self, card):
        if self.cards > 11 and self.armoured:  # if it is the first turn and armour has not been removed
            choice = 5  # remove armour
        else:
            choice = 6  # put the card in the dungeon
        self.cards -= 1  # this play
        return choice

    def vorpal_choice(self, last_turn):
        return 5  # without using more memory, this is the best choice statistically

    def result(self, bot, result, dungeon, vorped):
        self.cards = 13
        self.armoured = True
