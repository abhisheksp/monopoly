from itertools import cycle
from unittest.mock import MagicMock, Mock

import utils
from adapter.agent import Agent
from game_phases.bsmt import BSMT
from game_phases.buy_property import BuyProperty
from game_phases.context import Context
from game_phases.dice_roll import DiceRoll
from game_phases.pay_rent import PayRent
from game_phases.square_effect import SquareEffect
from game_state.board import Board
from game_state.game_state import GameState
from game_state.player import Player


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


def demo():
    # Agent 1 always buys, Agent 2 does not buy properties
    agent_1 = Agent()
    agent_1.buy_property = MagicMock(return_value=True)
    agent_2 = Agent()
    agent_2.buy_property = MagicMock(return_value=False)

    context = setup(agent_1, agent_2)
    print(context.phase)
    print(context.state)

    # will be changed to terminal state based event looping
    num_moves = 100
    for _ in range(num_moves):
        context = context.apply()
        print(context.phase)
        print(context.state)


if __name__ == '__main__':
    demo()
