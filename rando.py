from base import BasePlayer
from random import randint
from random import choice
class RandomMandom(BasePlayer):
    def __init__(self):
        self.items = [0,1,2,3,4,5]

    def start_turn(self, last_turn):
        if last_turn in self.items:
            self.items.remove(last_turn)
        if len(self.items) > 0:
            return randint(0,1)
        return 1

    def play(self, card):
        if len(self.items) > 0:
            if randint(0,1) == 1:
                selection = choice(self.items)
                self.items.remove(selection)
                return selection
        return 6

    def vorpal_choice(self, last_turn):
        return choice([1,2,3,4,5,6,7,9])

    def result(self, bot, result, dungeon, vorped):
        # Never learns
        pass