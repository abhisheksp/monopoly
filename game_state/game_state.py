from itertools import cycle


class GameState:
    def __init__(self, players, board=None, bank=None):
        self.players = players
        self.players_iter = cycle(players)
        self.current_player = next(self.players_iter)
        self.board = board
        self.bank = bank

    def next_player(self):
        self.current_player = next(self.players_iter)

    def __repr__(self):
        state_str = '-----------------\n'
        state_str += 'Current Player: {}\n'.format(self.current_player)
        state_str += '{}'.format(self.board)
        state_str += '-----------------\n'
        return state_str
