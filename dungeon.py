##########################################
#                                        #
#   +--------------------------------+   #
#   |                                |   #
#   |         the dungeon of         |   #
#   |             botdom             |   #
#   |  - of crisis and martyrdom     |   #
#   |                                |   #
#   |  a king of the hill challenge  |   #
#   |                                |   #
#   |         - created by the lemon |   #
#   +--------------------------------+   #
#                                        #
##########################################


import botclasses
import random


class IllegalPlayError(Exception):
    pass


class DungeonController:
    BASE_DECK = (list(range(1, 6)) * 2) + [6, 7, 9]
    ROUNDS_TO_RESULT = 5
    GAMES = 1000
    # noinspection PyUnresolvedReferences
    # now there are no annoying squiggly lines here
    import random

    # Items:
    PACT = 0
    #         0: Demonic pact: "defeat" the demon (strength 7 monster), and the monster after it.
    #                      (no effect if the demon was the last in the dungeon)

    POTION = 1
    #         1: Health potion: When you fall to 0 hp, defeat the monster and return to 3hp

    GRAIL = 2
    #         2: Holy grail: Defeat monsters of even strength (in the game, these are undead).

    DAGGER = 3
    #         3: Vorpal dagger: Choose one monster before entering the dungeon. this type of monster is defeated

    SHIELD = 4
    #         4: Shield: +3 hp

    ARMOUR = 5
    #         5: Armour: +5 hp

    #         Base character: 3 hp (obviously cannot be discarded)

    DUNGEON = 6

    PASS = 7

    def __init__(self):
        self.bots_that_done_messed_up = []

    def turn(self, bot, last_turn, deck, dungeon, items):
        decision = bot.start_turn(last_turn)
        if decision == 1:
            card = deck.pop()
            choice = bot.play(card)
            if choice == self.DUNGEON:
                dungeon.append(card)
                turn = choice
            elif choice in range(6) and items[choice]:
                items[choice] = False
                turn = choice
            else:
                raise IllegalPlayError  # they made an invalid move
        else:
            turn = self.PASS
        return deck, dungeon, items, turn

    def round(self, first_bot, bots):
        deck = self.BASE_DECK[:]
        dungeon_cards = []
        items = [True for i in range(6)]
        random.shuffle(deck)
        bot_chosen = None
        last_turn = None
        index = first_bot
        while bot_chosen is None:
            try:
                play = self.turn(bots[index], last_turn, deck[:], dungeon_cards[:], items[:])
            except IllegalPlayError:
                return index, -1
            deck, dungeon_cards, items, last_turn = play
            index += 1
            index %= 2
            if last_turn == self.PASS or deck == []:
                bot_chosen = bots[index]
        if items[self.DAGGER]:
            vorped = bot_chosen.vorpal_choice(last_turn)
            if vorped not in self.BASE_DECK:
                return index, -1
        else:
            vorped = None
        hp = 3
        if items[self.SHIELD]:
            hp += 3
        if items[self.ARMOUR]:
            hp += 5
        pact_killing = False
        for card in dungeon_cards[::-1]:
            if pact_killing:
                pact_killing = False
            elif card == 7 and items[self.PACT]:
                pact_killing = True
            elif (not card % 2 == 0 and items[self.GRAIL]) and (card is not vorped):
                hp -= card
                if hp <= 0:
                    if items[self.POTION]:
                        hp = 3
                        items[self.POTION] = False
                    else:
                        break
        result = hp <= 0  # whether they failed
        bots[index].result(0, result)  # tell the bot that they ventured into the dungeon, and whether they failed

        bots[not index].result(1, result)
        # tell the bot that the other ventured into the dungeon
        # and whether they failed
        return index, result

    def game(self, bot_first, bot_class0, bot_class1):
        winner = None
        first_bot = bot_first
        bot0 = bot_class0()
        bot1 = bot_class1()
        scores = [[0, 0], [0, 0]]
        while all(all(results != self.ROUNDS_TO_RESULT for results in bot_score) for bot_score in scores):
            bot, result = self.round(first_bot, (bot0, bot1))
            if result == -1:
                if (bot0, bot1)[bot].__class__.__name__ not in self.bots_that_done_messed_up:
                    self.bots_that_done_messed_up.append((bot0, bot1)[bot].__class__.__name__)
                return not bot  # one bot played wrong so the other wins the game.
            scores[bot][result] += 1
            first_bot += 1
            first_bot %= 2

        for bot_index in (0, 1):
            if any(tally == self.ROUNDS_TO_RESULT for tally in scores[bot_index]):
                if scores[bot_index][0] == self.ROUNDS_TO_RESULT:
                    winner = bot_index
                else:
                    winner = 1 ^ bot_index
        return winner

    def match(self, bot_class0, bot_class1):
        bot_first = 0
        points = [0, 0]
        for i in range(self.GAMES):
            winner = self.game(bot_first, bot_class0, bot_class1)
            points[winner] += 1
            bot_first += 1
            bot_first %= 2
        return points

    def matchmaking(self, bot_list):
        num_matches = len(bot_list)*(len(bot_list)-1)/2  # fancy triangle number notation
        matches_done = 0
        scores = [0]*len(bot_list)
        for bot0 in range(len(bot_list)-1):
            for bot1 in range(bot0+1, len(bot_list)):
                results = self.match(bot_list[bot0], bot_list[bot1])
                scores[bot0] += results[0]
                scores[bot1] += results[1]
                matches_done += 1
                print("\r"+str(round(matches_done*100/num_matches, 1))+"%", end = '')
        print("\r")
        end_results = sorted([(scores[i], bot_list[i].__name__, round(scores[i]/(self.GAMES*(len(bot_list)-1)), 2))
                              for i in range(len(scores))], reverse =True)
        placings = []
        for i in range(len(end_results)):
            if i == 0:
                actual_placing = 1
            else:
                if end_results[i][0] == placings[-1][1]:
                    actual_placing = placings[-1][0]
                else:
                    actual_placing = i + 1
            placings += [(actual_placing, end_results[i][1], end_results[i][0], end_results[i][2])]
        print('\n'.join(' '.join(str(i) for i in bot_result) for bot_result in placings))
        if self.bots_that_done_messed_up:
            print("bots that done messed up:\n- "+'\n- '.join(self.bots_that_done_messed_up))


dungeon = DungeonController()  # more like dumb-geon. zing!
dungeon.matchmaking(botclasses.bot_list())
