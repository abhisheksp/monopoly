class Context:
    def __init__(self, phases, game_state, game_phase):
        self.state = game_state
        self.phase = game_phase
        self._phases = phases

    def get_phase(self, new_phase):
        return self._phases[new_phase]

    def apply(self, ):
        return self.phase.apply(self)
