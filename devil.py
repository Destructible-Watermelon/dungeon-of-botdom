from base import BasePlayer


class DareDevilDumDum(BasePlayer):
    def start_turn(self, last_turn):
        return 1  # damn squiggles

    def play(self, card):
        return 6+card*0  # put the card in the dungeon, and use card to avoid squiggles :P

    def vorpal_choice(self, last_turn):
        return 9+last_turn*0  # dragon

    def result(self, bot, result, dungeon, vorped):
        pass  # we live for the thrill, not the result!
