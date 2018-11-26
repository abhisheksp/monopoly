from unittest import mock
from unittest.mock import MagicMock

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


def test_1():
    agent_1 = player_1()
    agent_2 = player_2()
    dice_rolls = [(1, 2)]
    _, state = Adjudicator.runGame(agent_1, agent_2, dice_rolls)
    print(state)
    expected_state = (0, (0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), (1500, 1490), (3, 0), 'Turn End Phase', None, (0, 0, 0, 0), [])
    assert (state == expected_state)


if __name__ == '__main__':
    test_1()
