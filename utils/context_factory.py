from itertools import cycle
from unittest.mock import Mock

import utils
from game_phases import Context
from game_phases.auction import Auction
from game_phases.bsmt import BSMT
from game_phases.buy_property import BuyProperty
from game_phases.dice_roll import DiceRoll
from game_phases.mortgage_property import MortgageProperty
from game_phases.pay_rent import PayRent
from game_phases.square_effect import SquareEffect
from game_phases.turn_end import TurnEnd
from game_state.board import Board
from game_state.game_state import GameState
from game_state.player import Player


def context_factory(agent_1, agent_2, dice_rolls):
    dice = utils.Dice()
    roll_mock = Mock()
    roll_mock.side_effect = iter(dice_rolls)
    dice.roll = roll_mock
    dice_roll_phase = DiceRoll(dice)
    square_effect_phase = SquareEffect()
    bsmt_phase = BSMT()
    buy_property_phase = BuyProperty()
    pay_rent_phase = PayRent()
    auction_phase = Auction()
    turn_end_phase = TurnEnd()
    mortgage_property_phase = MortgageProperty()
    phases = {
        'DiceRoll': dice_roll_phase,
        'SquareEffect': square_effect_phase,
        'BSMT': bsmt_phase,
        'BuyProperty': buy_property_phase,
        'MortgageProperty': mortgage_property_phase,
        'PayRent': pay_rent_phase,
        'Auction': auction_phase,
        'TurnEnd': turn_end_phase,
    }
    board = Board()
    player_1 = Player(1, amount=1500, position=board.property_at(0), agent=agent_1)
    player_2 = Player(2, amount=1500, position=board.property_at(0), agent=agent_2)
    players = [player_1, player_2]
    game_state = GameState(players, board)
    start_phase = dice_roll_phase
    context = Context(phases, game_state, start_phase)
    return context
