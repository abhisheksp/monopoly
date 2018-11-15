from itertools import cycle


class GameState:
    def __init__(self, players, board=None):
        self.players = cycle(players)
        self.current_player = next(self.players)
        self.board = board

    def next_player(self):
        self.current_player = next(self.players)

    def __repr__(self):
        state_str = '-----------------\n'
        state_str += 'Current Player: {}\n'.format(self.current_player)
        state_str += '{}'.format(self.board)
        state_str += '-----------------\n'
        return state_str
