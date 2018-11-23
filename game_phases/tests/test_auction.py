from unittest import TestCase
from unittest.mock import MagicMock

from adapter.agent import Agent
from game_phases import Context
from game_phases.auction import Auction
from game_phases.bsmt import BSMT
from game_phases.square_effect import SquareEffect
from game_state.board import Board
from game_state.game_state import GameState
from game_state.player import Player


class AuctionTest(TestCase):
    def test_apply(self):
        square_effect_phase = SquareEffect()
        auction_phase = Auction()
        bsmt_phase = BSMT()
        phases = {
            'SquareEffect': square_effect_phase,
            'Auction': auction_phase,
            'BSMT': bsmt_phase,

        }
        board = Board()
        agent_1, agent_2 = Agent(), Agent()
        agent_1.auction_property = MagicMock(return_value=100)
        agent_2.auction_property = MagicMock(return_value=120)
        player_1 = Player(1, amount=500, position=board.property_at(1), agent=agent_1)
        player_2 = Player(2, amount=500, position=board.property_at(0), agent=agent_2)
        players = [player_1, player_2]

        game_state = GameState(players, board)
        game_phase = auction_phase
        context = Context(phases, game_state, game_phase)
        new_context, next_action = context.apply()
        current_position = new_context.state.current_player.position

        self.assertTrue(new_context.phase is bsmt_phase)
        self.assertTrue(current_position.owned_by is player_2)
        self.assertEqual(player_2.amount, 380)
        self.assertEqual(player_1.amount, 500)
