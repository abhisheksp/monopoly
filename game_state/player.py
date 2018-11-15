class Player:
    def __init__(self, id_, position=None, previous_rolls=None, agent=None):
        self.id = id_
        self.previous_rolls = previous_rolls
        if previous_rolls is None:
            self.previous_rolls = (0, 0), (0, 0)

        self.position = position
        self.agent = agent

    def update_roll(self, dice_roll):
        self.previous_rolls = self.previous_rolls[-1], dice_roll

    def update_position(self, new_position):
        self.position = new_position

    def double_roll(self):
        return self.previous_rolls[-1][0] == self.previous_rolls[-1][1]
