class Player:
    def __init__(self, id_, previous_rolls=None):
        self.id = id_
        self.previous_rolls = previous_rolls
        if previous_rolls is None:
            self.previous_rolls = (0, 0), (0, 0)

    def update_roll(self, dice_roll):
        self.previous_rolls = self.previous_rolls[-1], dice_roll

    def double_roll(self):
        return self.previous_rolls[-1][0] == self.previous_rolls[-1][1]
