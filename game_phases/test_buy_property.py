from unittest import TestCase
from unittest.mock import MagicMock

from adapter.agent import Agent
from game_phases.bsmt import BSMT
from game_phases.buy_property import BuyProperty
from game_phases.context import Context
from game_state.board import Board
from game_state.game_state import GameState
from game_state.player import Player


class TestBuyProperty(TestCase):
    def test_player_buys_property(self):
        buy_property_phase = BuyProperty()
        bsmt_phase = BSMT()
        phases = {
            'BuyProperty': buy_property_phase,
            'BSMT': bsmt_phase,
        }
        board = Board()
        agent = Agent()
        agent.buy_property = MagicMock(return_value=True)
        player_1 = Player(1, position=board.property_at(1), agent=agent)
        player_2 = Player(2, position=board.property_at(0))
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_phase = buy_property_phase
        context = Context(phases, game_state, game_phase)
        new_context = context.apply()

        self.assertTrue(new_context.phase is bsmt_phase)
        self.assertTrue(new_context.state.current_player.position.owned_by is player_1)
