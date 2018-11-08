from itertools import cycle


class GameState:
    def __init__(self, players):
        self.players = cycle(players)
        self.current_player = next(self.players)

    def next_player(self):
        self.current_player = next(self.players)
