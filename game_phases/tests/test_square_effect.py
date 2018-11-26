import unittest

from game_phases.bsmt import BSMT
from game_phases.buy_property import BuyProperty
from game_phases.context import Context
from game_phases.dice_roll import DiceRoll
from game_phases.pay_rent import PayRent
from game_phases.square_effect import SquareEffect
from game_state.board import Board
from game_state.game_state import GameState
from game_state.player import Player


class SquareEffectTest(unittest.TestCase):
    def test_unowned_property(self):
        dice_roll_phase = DiceRoll()
        square_effect_phase = SquareEffect()
        buy_property_phase = BuyProperty()
        pay_rent_phase = PayRent()
        phases = {
            'DiceRoll': dice_roll_phase,
            'SquareEffect': square_effect_phase,
            'BuyProperty':  buy_property_phase,
            'PayRent': pay_rent_phase,
        }
        board = Board()
        player_1 = Player(1, position=board.property_at(1))
        player_2 = Player(2, position=board.property_at(1))
        players = [player_1, player_2]
        game_state = GameState(players)
        game_phase = square_effect_phase
        context = Context(phases, game_state, game_phase)
        new_context, next_action = context.apply()

        self.assertTrue(isinstance(new_context.phase, BuyProperty))

    def test_self_owned_property(self):
        bsmt_phase = BSMT()
        square_effect_phase = SquareEffect()
        buy_property_phase = BuyProperty()
        pay_rent_phase = PayRent()
        phases = {
            'BSMT': bsmt_phase,
            'SquareEffect': square_effect_phase,
            'BuyProperty':  buy_property_phase,
            'PayRent': pay_rent_phase,
        }
        board = Board()
        player_1 = Player(1, position=board.property_at(1))
        player_2 = Player(2, position=board.property_at(1))
        mediterranean_avenue = board.property_at(1)
        mediterranean_avenue.own(player_1)
        players = [player_1, player_2]
        game_state = GameState(players)
        game_phase = square_effect_phase
        context = Context(phases, game_state, game_phase)
        new_context, next_action = context.apply()

        self.assertTrue(new_context.phase is bsmt_phase)

    def test_opponent_owned_property(self):
        dice_roll_phase = DiceRoll()
        square_effect_phase = SquareEffect()
        buy_property_phase = BuyProperty()
        pay_rent_phase = PayRent()
        phases = {
            'DiceRoll': dice_roll_phase,
            'SquareEffect': square_effect_phase,
            'BuyProperty':  buy_property_phase,
            'PayRent': pay_rent_phase,
        }
        board = Board()
        player_1 = Player(1, position=board.property_at(1))
        player_2 = Player(2, position=board.property_at(1))
        mediterranean_avenue = board.property_at(1)
        mediterranean_avenue.own(player_2)
        players = [player_1, player_2]
        game_state = GameState(players)
        game_phase = square_effect_phase
        context = Context(phases, game_state, game_phase)
        new_context, next_action = context.apply()

        self.assertTrue(isinstance(new_context.phase, PayRent))


if __name__ == '__main__':
    unittest.main()
