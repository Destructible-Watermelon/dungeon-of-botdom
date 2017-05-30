class BasePlayer:
    def start_turn(self, last_turn):
        raise NotImplementedError

    def play(self, card):
        raise NotImplementedError

    def vorpal_choice(self, last_turn):
        raise NotImplementedError

    def result(self, bot, result):
        raise NotImplementedError
