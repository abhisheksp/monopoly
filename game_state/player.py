class Player:
    def __init__(self, id_, amount=0, position=None, previous_rolls=None, agent=None):
        self.id = id_
        self.previous_rolls = previous_rolls
        if previous_rolls is None:
            self.previous_rolls = (0, 0), (0, 0)

        self.position = position
        self.agent = agent
        self.amount = amount

    def pay_rent(self, rent):
        self.amount -= rent

    def buy_property(self, cost):
        self.amount -= cost

    def update_roll(self, dice_roll):
        self.previous_rolls = self.previous_rolls[-1], dice_roll

    def update_position(self, new_position):
        self.position = new_position

    def double_roll(self):
        return self.previous_rolls[-1][0] == self.previous_rolls[-1][1]

    def __repr__(self):
        repr_str = 'ID: {}\n'.format(self.id)
        repr_str += 'Rolled : {}\n'.format(self.previous_rolls[-1])
        repr_str += 'Currently at : {}\n'.format(self.position)
        return repr_str
