from unittest import TestCase
from unittest.mock import MagicMock

from game_phases import Context
from game_phases.bsmt import BSMT
from game_phases.buy_property import BuyProperty
from game_phases.special_property import SpecialProperty
from game_state.board import Board
from game_state.game_state import GameState
from game_state.player import Player
import utils


class SpecialPropertyTest(TestCase):
    def test_chance_0(self):
        bsmt_phase = BSMT()
        special_property_phase = SpecialProperty()
        phases = {
            'BSMT': bsmt_phase,
            'SpecialProperty': special_property_phase,
        }
        board = Board()
        board.next_chance = MagicMock(return_value=0)
        player_1 = Player(1, amount=200, position=board.property_at(1))
        player_2 = Player(2, amount=200, position=board.property_at(36))
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_state.next_player()
        game_phase = special_property_phase
        context = Context(phases, game_state, game_phase)
        new_context, next_action = context.apply()
        go = board.property_at(0)

        self.assertTrue(new_context.phase is bsmt_phase)
        self.assertTrue(player_2.position is go)
        self.assertEqual(player_2.amount, 400)
        self.assertEqual(player_1.amount, 200)

    def test_chance_1(self):
        bsmt_phase = BSMT()
        special_property_phase = SpecialProperty()
        phases = {
            'BSMT': bsmt_phase,
            'SpecialProperty': special_property_phase,
        }
        board = Board()
        board.next_chance = MagicMock(return_value=1)
        board.passes_go = MagicMock(return_value=True)
        player_1 = Player(1, amount=100, position=board.property_at(1))
        player_2 = Player(2, amount=300, position=board.property_at(36))
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_state.next_player()
        game_phase = special_property_phase
        context = Context(phases, game_state, game_phase)
        new_context, next_action = context.apply()
        illinois_avenue = board.property_at(24)

        self.assertTrue(new_context.phase is bsmt_phase)
        self.assertTrue(player_2.position is illinois_avenue)
        self.assertEqual(player_2.amount, 500)
        self.assertEqual(player_1.amount, 100)

    def test_chance_2(self):
        bsmt_phase = BSMT()
        special_property_phase = SpecialProperty()
        phases = {
            'BSMT': bsmt_phase,
            'SpecialProperty': special_property_phase,
        }
        board = Board()
        board.next_chance = MagicMock(return_value=2)
        board.passes_go = MagicMock(return_value=True)
        player_1 = Player(1, amount=100, position=board.property_at(1))
        player_2 = Player(2, amount=300, position=board.property_at(36))
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_state.next_player()
        game_phase = special_property_phase
        context = Context(phases, game_state, game_phase)
        st_charles_place = board.property_at(11)

        new_context, next_action = context.apply()

        self.assertTrue(new_context.phase is bsmt_phase)
        self.assertTrue(player_2.position is st_charles_place)
        self.assertEqual(player_2.amount, 500)
        self.assertEqual(player_1.amount, 100)

    def test_chance_3_unowned(self):
        special_property_phase = SpecialProperty()
        buy_property_phase = BuyProperty()
        phases = {
            'SpecialProperty': special_property_phase,
            'BuyProperty': buy_property_phase
        }
        board = Board()
        board.next_chance = MagicMock(return_value=3)
        electric_company = board.property_at(12)
        board.nearest_utility = MagicMock(return_value=electric_company)
        player_1 = Player(1, amount=100, position=board.property_at(0))
        player_2 = Player(2, amount=300, position=board.property_at(36))
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_state.next_player()
        game_phase = special_property_phase
        context = Context(phases, game_state, game_phase)

        new_context, next_action = context.apply()

        self.assertTrue(new_context.phase is buy_property_phase)
        self.assertTrue(player_2.position is electric_company)
        self.assertEqual(player_2.amount, 300)
        self.assertEqual(player_1.amount, 100)

    def test_chance_3_owned(self):
        dice = utils.Dice()
        dice.roll = MagicMock(return_value=(1, 2))
        special_property_phase = SpecialProperty(dice)
        bsmt_phase = BSMT()
        phases = {
            'SpecialProperty': special_property_phase,
            'BSMT': bsmt_phase
        }
        board = Board()
        board.next_chance = MagicMock(return_value=3)
        electric_company = board.property_at(12)
        board.nearest_utility = MagicMock(return_value=electric_company)
        player_1 = Player(1, amount=100, position=board.property_at(0))
        player_2 = Player(2, amount=300, position=board.property_at(36))
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_state.next_player()
        game_phase = special_property_phase
        context = Context(phases, game_state, game_phase)
        electric_company.own(player_1)

        new_context, next_action = context.apply()

        self.assertTrue(new_context.phase is bsmt_phase)
        self.assertTrue(player_2.position is electric_company)
        self.assertEqual(player_2.amount, 300 - 10 * 3)
        self.assertEqual(player_1.amount, 100 + 10 * 3)

    def test_chance_4_5_unowned(self):
        special_property_phase = SpecialProperty()
        buy_property_phase = BuyProperty()
        phases = {
            'SpecialProperty': special_property_phase,
            'BuyProperty': buy_property_phase
        }
        board = Board()
        board.next_chance = MagicMock(return_value=4)
        reading_railroad = board.property_at(5)
        board.nearest_railroad = MagicMock(return_value=reading_railroad)
        player_1 = Player(1, amount=100, position=board.property_at(0))
        player_2 = Player(2, amount=300, position=board.property_at(36))
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_state.next_player()
        game_phase = special_property_phase
        context = Context(phases, game_state, game_phase)

        new_context, next_action = context.apply()

        self.assertTrue(new_context.phase is buy_property_phase)
        self.assertTrue(player_2.position is reading_railroad)
        self.assertEqual(player_2.amount, 300)
        self.assertEqual(player_1.amount, 100)

    def test_chance_4_5_owned(self):
        dice = utils.Dice()
        dice.roll = MagicMock(return_value=(1, 2))
        special_property_phase = SpecialProperty(dice)
        bsmt_phase = BSMT()
        phases = {
            'SpecialProperty': special_property_phase,
            'BSMT': bsmt_phase
        }
        board = Board()
        board.next_chance = MagicMock(return_value=4)
        reading_railroad = board.property_at(5)
        board.nearest_railroad = MagicMock(return_value=reading_railroad)
        player_1 = Player(1, amount=100, position=board.property_at(0))
        player_2 = Player(2, amount=300, position=board.property_at(36))
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_state.next_player()
        game_phase = special_property_phase
        context = Context(phases, game_state, game_phase)
        reading_railroad.own(player_1)
        reading_railroad.rent = MagicMock(return_value=15)

        new_context, next_action = context.apply()

        self.assertTrue(new_context.phase is bsmt_phase)
        self.assertTrue(player_2.position is reading_railroad)
        self.assertEqual(player_2.amount, 300 - 10 * 15)
        self.assertEqual(player_1.amount, 100 + 10 * 15)

    def test_chance_12(self):
        bsmt_phase = BSMT()
        special_property_phase = SpecialProperty()
        phases = {
            'BSMT': bsmt_phase,
            'SpecialProperty': special_property_phase,
        }
        board = Board()
        board.next_chance = MagicMock(return_value=12)
        board.passes_go = MagicMock(return_value=True)
        player_1 = Player(1, amount=100, position=board.property_at(1))
        player_2 = Player(2, amount=300, position=board.property_at(36))
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_state.next_player()
        game_phase = special_property_phase
        context = Context(phases, game_state, game_phase)
        new_context, next_action = context.apply()
        reading_railroad = board.property_at(5)

        self.assertTrue(new_context.phase is bsmt_phase)
        self.assertTrue(player_2.position is reading_railroad)
        self.assertEqual(player_2.amount, 500)
        self.assertEqual(player_1.amount, 100)

    def test_chance_13(self):
        bsmt_phase = BSMT()
        special_property_phase = SpecialProperty()
        phases = {
            'BSMT': bsmt_phase,
            'SpecialProperty': special_property_phase,
        }
        board = Board()
        board.next_chance = MagicMock(return_value=13)
        player_1 = Player(1, amount=100, position=board.property_at(1))
        player_2 = Player(2, amount=300, position=board.property_at(36))
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_state.next_player()
        game_phase = special_property_phase
        context = Context(phases, game_state, game_phase)
        new_context, next_action = context.apply()
        board_walk = board.property_at(39)

        self.assertTrue(new_context.phase is bsmt_phase)
        self.assertTrue(player_2.position is board_walk)
        self.assertEqual(player_2.amount, 300)
        self.assertEqual(player_1.amount, 100)
