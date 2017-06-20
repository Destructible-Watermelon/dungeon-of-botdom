from base import BasePlayer

class SlapAndFlap(BasePlayer):

    def reset(self):
        # Monsters that you pushed in
        self.know_monster = list(self.deck)

        # Items still in game
        self.items_in_game = [True, True, True, True, True, True]

        # List of items, sorted by value
        self.valuables = [3,1,5,0,2,4]

        # Counter
        self.cards = 13

    def __init__(self):
        # Deck
        self.deck = (1,1,2,2,3,3,4,4,5,5,6,7,9)
        # Indexes of item cards
        self.items = (0, 1, 2, 3, 4, 5)

        self.reset()

    def start_turn(self, last_turn):
        if last_turn is not None:
            self.cards -= 1

        # Sneak peak at items removed by opponent
        if last_turn is not None and  last_turn < 6:
            self.items_in_game[last_turn] = False
            self.valuables.remove(last_turn)

        # Flap!
        if self.cards < 6:
            return 0
        return 1

    def play(self, card):
        if card < 6 and any(self.items_in_game):
            self.know_monster.remove(card)
            to_return = self.valuables[0]   # remove the best of the rest
            self.valuables = self.valuables[1:]
            self.items_in_game[to_return] = False
            return to_return
        else:
            return 6

    def vorpal_choice(self, last_turn):
        # We can just guess what monster will be there
        # But we know ones, we removed

        # If we have pact, no need to remove demon
        if self.items_in_game[0]:
            self.know_monster.remove(7)
        # If we have grail, no need to remove even monsters (kinda)
        if self.items_in_game[2]:
            self.know_monster = [i for i in self.know_monster if i%2]

        # Find what threatens us the most, counting its strength multiplied by number
        weight = [i * self.know_monster.count(i) for i in self.know_monster]
        return weight.index(max(weight)) + 1


    def result(self, bot, result, dungeon, vorped):
        self.reset()  # we live for the thrill, not the result!