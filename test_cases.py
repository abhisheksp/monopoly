from unittest import mock
from unittest.mock import MagicMock, Mock

from adapter.adjudicator import Adjudicator
from adapter.agent import Agent


def player_1():
    external_agent = mock.Mock()
    external_agent.buyProperty = MagicMock(return_value=False)
    external_agent.auctionProperty = MagicMock(return_value=0)
    external_agent.getBMSTDecision = MagicMock(return_value=(None, None))
    return Agent(external_agent)


def player_2():
    external_agent = mock.Mock()
    external_agent.buyProperty = MagicMock(return_value=False)
    external_agent.auctionProperty = MagicMock(return_value=10)
    external_agent.getBMSTDecision = MagicMock(return_value=(None, None))
    return Agent(external_agent)


def player_3():
    external_agent = mock.Mock()
    external_agent.buyProperty = MagicMock(return_value=True)
    bsmt_decision_mock = Mock()
    bsmt_decision_mock.side_effect = iter([(None, None), ('M', [3]), (None, None), (None, None)])
    external_agent.getBMSTDecision = bsmt_decision_mock
    return Agent(external_agent)


def player_4():
    external_agent = mock.Mock()
    external_agent.buyProperty = MagicMock(return_value=False)
    external_agent.getBMSTDecision = MagicMock(return_value=(None, None))
    return Agent(external_agent)


def test_1():
    agent_1 = player_1()
    agent_2 = player_2()
    dice_rolls = [(1, 2)]
    _, state = Adjudicator.runGame(agent_1, agent_2, dice_rolls)
    expected_state = (0, (
        0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0,
        0, 0, 0, 0), (1500, 1490), (3, 0), 'Turn End Phase', None, (0, 0, 0, 0), [])
    assert (state == expected_state)


def test_2():
    agent_1 = player_3()
    agent_2 = player_4()
    dice_rolls = [(1, 2), (1, 2)]
    _, state = Adjudicator.runGame(agent_1, agent_2, dice_rolls)
    expected_state = (0, (
        0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0,
        0, 0, 0), (1470.0, 1500), (3, 3), 'Turn End Phase', None, (0, 0, 0, 0), [])
    assert (state == expected_state)


def test_3():
    agent_1 = player_1()
    agent_2 = player_2()
    dice_rolls = [(6, 1), (1, 6), (1, 6)]
    _, state = Adjudicator.runGame(agent_1, agent_2, dice_rolls)
    expected_state = (0, (
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0), (1700, 1500), (11, 24), 'Turn End Phase', None, (0, 0, 0, 0), [])
    assert (state == expected_state)


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
