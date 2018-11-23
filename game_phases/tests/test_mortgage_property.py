from unittest import TestCase

from game_phases import Context
from game_phases.bsmt import BSMT
from game_phases.mortgage_property import MortgageProperty
from game_state.bank import Bank
from game_state.board import Board
from game_state.game_state import GameState
from game_state.player import Player
from game_state.property_type import PropertyType


class MortgagePropertyTest(TestCase):
    def test_mortgage_property(self):
        mortgage_property_phase = MortgageProperty()
        bsmt_phase = BSMT()
        phases = {
            'MortgagePropertyHouse': mortgage_property_phase,
            'BSMT': bsmt_phase,
        }
        board = Board()
        player_1 = Player(1, amount=500, position=board.property_at(1))
        player_2 = Player(2, amount=500, position=board.property_at(0))
        players = [player_1, player_2]
        mediterranean_avenue = board.property_at(1)
        mediterranean_avenue.own(player_1)
        mediterranean_avenue.mortgage_value = 200
        bank = Bank()
        game_state = GameState(players, board, bank=bank)
        game_phase = mortgage_property_phase
        context = Context(phases, game_state, game_phase)
        action = mediterranean_avenue

        new_context, next_action = context.apply(action)

        self.assertTrue(new_context.phase is bsmt_phase)
        self.assertTrue(mediterranean_avenue.type is PropertyType.MORTGAGED)
        self.assertEqual(player_1.amount, 700)
        self.assertEqual(player_2.amount, 500)

    def test_unmortgage_property(self):
        mortgage_property_phase = MortgageProperty()
        bsmt_phase = BSMT()
        phases = {
            'MortgagePropertyHouse': mortgage_property_phase,
            'BSMT': bsmt_phase,
        }
        board = Board()
        player_1 = Player(1, amount=500, position=board.property_at(1))
        player_2 = Player(2, amount=500, position=board.property_at(0))
        players = [player_1, player_2]
        mediterranean_avenue = board.property_at(1)
        mediterranean_avenue.mortgage_value = 200
        mediterranean_avenue.own(player_1)
        mediterranean_avenue.mortgage()
        bank = Bank()
        game_state = GameState(players, board, bank=bank)
        game_phase = mortgage_property_phase
        context = Context(phases, game_state, game_phase)
        action = mediterranean_avenue

        new_context, next_action = context.apply(action)

        self.assertTrue(new_context.phase is bsmt_phase)
        self.assertTrue(mediterranean_avenue.type is PropertyType.OWNED)
        self.assertEqual(player_1.amount, 280)
        self.assertEqual(player_2.amount, 500)
