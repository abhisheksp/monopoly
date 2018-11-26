import unittest
from itertools import cycle
from unittest import TestCase
from unittest.mock import Mock

from game_phases.bsmt import BSMT

import utils
from adapter.agent import Agent
from game_phases import Context
from game_phases.buy_property import BuyProperty
from game_phases.dice_roll import DiceRoll
from game_phases.pay_rent import PayRent
from game_phases.square_effect import SquareEffect
from game_state.board import Board
from game_state.game_state import GameState
from game_state.player import Player
import adapter.game_state


class GameStateTest(TestCase):
    def test_properties(self):
        board = Board()
        player = Player(4)
        result = adapter.game_state.properties_tuple(board._squares, player)
        expected = tuple([0] * 42)

        self.assertEqual(result, expected)

    def test_parse(self):
        self.skipTest('wip')
        agent_1, agent_2 = Agent(), Agent()
        context = setup(agent_1, agent_2)

        game_state = adapter.game_state.parse(context)

        self.assertEqual(game_state, None)


def setup(agent_1, agent_2):
    dice = utils.Dice()
    roll_mock = Mock()
    roll_mock.side_effect = cycle([(1, 2), (2, 2)])
    dice.roll = roll_mock
    dice_roll_phase = DiceRoll(dice)
    square_effect_phase = SquareEffect()
    bsmt_phase = BSMT()
    buy_property_phase = BuyProperty()
    pay_rent_phase = PayRent()
    phases = {
        'DiceRoll': dice_roll_phase,
        'SquareEffect': square_effect_phase,
        'BSMT': bsmt_phase,
        'BuyProperty': buy_property_phase,
        'PayRent': pay_rent_phase,
    }
    board = Board()
    player_1 = Player(1, position=board.property_at(0), agent=agent_1)
    player_2 = Player(2, position=board.property_at(0), agent=agent_2)
    players = [player_1, player_2]
    game_state = GameState(players, board)
    start_phase = dice_roll_phase
    context = Context(phases, game_state, start_phase)
    return context


if __name__ == '__main__':
    unittest.main()
