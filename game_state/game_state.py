from itertools import cycle


class GameState:
    def __init__(self, players, board=None):
        self.players = cycle(players)
        self.current_player = next(self.players)
        self.board = board

    def next_player(self):
        self.current_player = next(self.players)
