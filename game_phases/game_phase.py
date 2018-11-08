import abc


class GamePhase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def apply(self, game_state, action=None):
        return self
