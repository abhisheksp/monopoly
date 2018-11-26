from unittest import TestCase
from unittest.mock import MagicMock

from adapter.agent import Agent
from game_phases.auction import Auction
from game_phases.bsmt import BSMT
from game_phases.buy_property import BuyProperty
from game_phases.context import Context
from game_state.board import Board
from game_state.game_state import GameState
from game_state.player import Player


class BuyPropertyTest(TestCase):
    @staticmethod
    def fake_bsmt_cycle(amount):
        def return_func(context, _):
            context.state.current_player.increment(amount)
            return context, None
        return return_func

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
        current_position = board.property_at(1)
        current_position.cost = 100
        player_1 = Player(1, amount=20, position=current_position, agent=agent)
        player_2 = Player(2)
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_phase = buy_property_phase
        context = Context(phases, game_state, game_phase)
        bsmt_phase.apply = self.fake_bsmt_cycle(100)

        new_context, next_action = context.apply()

        self.assertTrue(new_context.phase is bsmt_phase)
        self.assertTrue(new_context.state.current_player.position.owned_by is player_1)
        self.assertEqual(new_context.state.current_player.amount, 20)
        self.assertEqual(new_context.state.current_player._debt['bank'], 0)

    def test_player_declines_buying_property(self):
        buy_property_phase = BuyProperty()
        bsmt_phase = BSMT()
        auction_phase = Auction()
        phases = {
            'BuyProperty': buy_property_phase,
            'BSMT': bsmt_phase,
            'Auction': auction_phase,
        }
        board = Board()
        agent = Agent()
        agent.buy_property = MagicMock(return_value=False)
        player_1 = Player(1, amount=900, position=board.property_at(1), agent=agent)
        player_2 = Player(2, position=board.property_at(0))
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_phase = buy_property_phase
        context = Context(phases, game_state, game_phase)
        new_context, next_action = context.apply()

        self.assertTrue(new_context.phase is auction_phase)
        self.assertEqual(new_context.state.current_player.amount, 900)
