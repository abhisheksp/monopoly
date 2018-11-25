from unittest import TestCase
from unittest.mock import MagicMock, Mock

from adapter.agent import Agent
from game_phases.bsmt import BSMT
from game_phases.buy_house import BuyHouse
from game_phases.context import Context
from game_phases.dice_roll import DiceRoll
from game_phases.mortgage_property import MortgageProperty
from game_phases.sell_house import SellHouse
from game_phases.trade_property import TradeProperty
from game_state.action import Action
from game_state.board import Board
from game_state.game_state import GameState
from game_state.player import Player


class BSMTTest(TestCase):
    def test_buy_house_action(self):
        bsmt_phase = BSMT()
        buy_house_phase = BuyHouse()
        dice_roll_phase = DiceRoll()
        phases = {
            'BuyHouse': buy_house_phase,
            'BSMT': bsmt_phase,
            'DiceRoll': dice_roll_phase,
        }

        board = Board()
        agent_1 = Agent()
        buy_action = [1, 2]
        agent_1_mock = Mock()
        agent_1_mock.side_effect = iter([(Action.BUY_HOUSE, buy_action), (None, None)])
        agent_1.bsmt_decision = agent_1_mock
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
        buy_house_phase.apply = MagicMock(return_value=context)
        context.apply()

        buy_house_phase.apply.assert_called_once()

    def test_sell_house_action(self):
        bsmt_phase = BSMT()
        sell_house_phase = SellHouse()
        dice_roll_phase = DiceRoll()
        phases = {
            'SellHouse': sell_house_phase,
            'BSMT': bsmt_phase,
            'DiceRoll': dice_roll_phase,
        }
        board = Board()
        agent_1 = Agent()
        agent_1.bsmt_decision = MagicMock(return_value=(None, None))
        agent_2 = Agent()
        sell_action = [1, 1]
        agent_2_mock = Mock()
        agent_2_mock.side_effect = iter([(Action.SELL_HOUSE, sell_action), (None, None)])
        agent_2.bsmt_decision = agent_2_mock
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
        sell_house_phase.apply = MagicMock(return_value=context)

        context.apply()

        sell_house_phase.apply.assert_called_once()

    def test_mortgage_property_action(self):
        bsmt_phase = BSMT()
        mortgage_property_phase = MortgageProperty()
        dice_roll_phase = DiceRoll()
        phases = {
            'MortgageProperty': mortgage_property_phase,
            'BSMT': bsmt_phase,
            'DiceRoll': dice_roll_phase,

        }
        board = Board()
        agent_1 = Agent()
        agent_2 = Agent()
        player_1 = Player(1, position=board.property_at(0), agent=agent_1)
        player_2 = Player(2, position=board.property_at(1), agent=agent_2)
        mediterranean_avenue = board.property_at(1)
        mediterranean_avenue.build(2)
        mediterranean_avenue.own(player_2)
        agent_1.bsmt_decision = MagicMock(return_value=(None, None))
        agent_2_mock = Mock()
        agent_2_mock.side_effect = iter([(Action.MORTGAGE_PROPERTY, mediterranean_avenue), (None, None)])
        agent_2.bsmt_decision = agent_2_mock
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_state.next_player()
        game_phase = bsmt_phase
        context = Context(phases, game_state, game_phase)
        mortgage_property_phase.apply = MagicMock(return_value=context)

        context.apply()

        mortgage_property_phase.apply.assert_called_once()

    def test_trade_property_action(self):
        bsmt_phase = BSMT()
        trade_property_phase = TradeProperty()
        dice_roll_phase = DiceRoll()
        phases = {
            'TradeProperty': trade_property_phase,
            'BSMT': bsmt_phase,
            'DiceRoll': dice_roll_phase,

        }
        board = Board()
        agent_1 = Agent()
        agent_2 = Agent()
        player_1 = Player(1, position=board.property_at(0), agent=agent_1)
        player_2 = Player(2, position=board.property_at(1), agent=agent_2)
        mediterranean_avenue = board.property_at(1)
        mediterranean_avenue.own(player_1)
        baltic_avenue = board.property_at(3)
        baltic_avenue.own(player_1)
        reading_railroad = board.property_at(5)
        reading_railroad.own(player_2)
        oriental_avenue = board.property_at(6)
        oriental_avenue.own(player_2)
        agent_1_mock = Mock()
        agent_1_mock.side_effect = iter([
            (
                Action.TRADE_PROPERTY,
                (200, [mediterranean_avenue, baltic_avenue], 400, [reading_railroad, oriental_avenue])
            ),
            (None, None)
        ])
        agent_1.bsmt_decision = agent_1_mock
        agent_2.bsmt_decision = MagicMock(return_value=(None, None))
        agent_2.respond_trade = MagicMock(return_value=(True, None))
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_state.next_player()
        game_phase = bsmt_phase
        context = Context(phases, game_state, game_phase)
        trade_property_phase.apply = MagicMock(return_value=context)
        expected_trades = [
            {'buyer': player_2, 'seller': player_1, 'price': 200, 'properties': [mediterranean_avenue, baltic_avenue]},
            {'buyer': player_1, 'seller': player_2, 'price': 400, 'properties': [reading_railroad, oriental_avenue]}
        ]

        context.apply()

        trade_property_phase.apply.assert_called_once_with(context, expected_trades)

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
        player_2 = Player(2, position=board.property_at(0), agent=agent)
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
        player_2 = Player(2, position=board.property_at(0), agent=agent)
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_phase = bsmt_phase
        context = Context(phases, game_state, game_phase)

        new_context, next_action = context.apply()

        self.assertTrue(new_context.phase is dice_roll_phase)
        self.assertTrue(new_context.state.current_player is player_1)
