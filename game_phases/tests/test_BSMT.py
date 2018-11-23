from unittest import TestCase
from unittest.mock import MagicMock

from adapter.agent import Agent
from game_phases.bsmt import BSMT
from game_phases.buy_house import BuyHouse
from game_phases.context import Context
from game_phases.dice_roll import DiceRoll
from game_phases.sell_house import SellHouse
from game_state.action import Action
from game_state.board import Board
from game_state.game_state import GameState
from game_state.player import Player


class BSMTTest(TestCase):
    def test_buy_house_action(self):
        bsmt_phase = BSMT()
        buy_house_phase = BuyHouse()
        phases = {
            'BuyHouse': buy_house_phase,
            'BSMT': bsmt_phase,
        }
        board = Board()
        agent_1 = Agent()
        buy_action = [1, 2]
        agent_1.bsmt_decision = MagicMock(return_value=(Action.BUY_HOUSE, buy_action))
        agent_2 = Agent()
        agent_2.bsmt_decision = MagicMock(return_value=(None, None))
        player_1 = Player(1, position=board.property_at(0), agent=agent_2)
        player_2 = Player(2, position=board.property_at(1), agent=agent_1)
        mediterranean_avenue = board.property_at(1)
        mediterranean_avenue.own(player_2)
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_state.next_player()
        game_phase = bsmt_phase
        context = Context(phases, game_state, game_phase)
        new_context, next_action = context.apply()
        self.assertTrue(new_context.phase is buy_house_phase)
        self.assertEqual(next_action, (mediterranean_avenue, 'House', 2))

    def test_sell_house_action(self):
        bsmt_phase = BSMT()
        sell_house_phase = SellHouse()
        phases = {
            'SellHouse': sell_house_phase,
            'BSMT': bsmt_phase,
        }
        board = Board()
        agent_1 = Agent()
        agent_1.bsmt_decision = MagicMock(return_value=(None, None))
        agent_2 = Agent()
        sell_action = [1, 1]
        agent_2.bsmt_decision = MagicMock(return_value=(Action.SELL_HOUSE, sell_action))
        player_1 = Player(1, position=board.property_at(0), agent=agent_1)
        player_2 = Player(2, position=board.property_at(1), agent=agent_2)
        mediterranean_avenue = board.property_at(1)
        mediterranean_avenue.build(2)
        mediterranean_avenue.own(player_2)
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_state.next_player()
        game_phase = bsmt_phase
        context = Context(phases, game_state, game_phase)
        new_context, next_action = context.apply()
        self.assertTrue(new_context.phase is sell_house_phase)
        self.assertEqual(next_action, (mediterranean_avenue, 'House', 1))

    def test_change_player_on_regular_roll(self):
        dice_roll_phase = DiceRoll()
        bsmt_phase = BSMT()
        phases = {
            'DiceRoll': dice_roll_phase,
            'BSMT': bsmt_phase,
        }
        board = Board()
        regular_roll = ((1, 2), (2, 3))
        agent = Agent()
        agent.bsmt_decision = MagicMock(return_value=(None, None))
        player_1 = Player(1, position=board.property_at(1), previous_rolls=regular_roll, agent=agent)
        player_2 = Player(2, position=board.property_at(0))
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_phase = bsmt_phase
        context = Context(phases, game_state, game_phase)
        new_context, next_action = context.apply()

        self.assertTrue(new_context.phase is dice_roll_phase)
        self.assertTrue(new_context.state.current_player is player_2)

    def test_change_player_on_double_roll(self):
        dice_roll_phase = DiceRoll()
        bsmt_phase = BSMT()
        phases = {
            'DiceRoll': dice_roll_phase,
            'BSMT': bsmt_phase,
        }
        board = Board()
        double_roll = ((1, 2), (2, 2))
        agent = Agent()
        agent.bsmt_decision = MagicMock(return_value=(None, None))
        player_1 = Player(1, position=board.property_at(1), previous_rolls=double_roll, agent=agent)
        player_2 = Player(2, position=board.property_at(0))
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_phase = bsmt_phase
        context = Context(phases, game_state, game_phase)
        new_context, next_action = context.apply()

        self.assertTrue(new_context.phase is dice_roll_phase)
        self.assertTrue(new_context.state.current_player is player_1)
