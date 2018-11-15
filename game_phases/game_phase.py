import abc


class GamePhase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def apply(self, game_context, action=None):
        return self
