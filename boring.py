from base import BasePlayer

class BoringPlayer(BasePlayer):
    def start_turn(self, last_turn):
        return 1

    def play(self, card):
        return 6

    def vorpal_choice(self, last_turn):
        return 5

    def result(self, bot, result, dungeon, vorped):
        # Never learns
        pass