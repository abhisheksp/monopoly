class Player:
    def __init__(self, id_, amount=0, position=None, previous_rolls=None, agent=None):
        self.id = id_
        self.previous_rolls = previous_rolls
        if previous_rolls is None:
            self.previous_rolls = (0, 0), (0, 0)

        self.position = position
        self.agent = agent
        self.amount = amount
        self._debt = {'bank': 0, 'opponents': 0}

    def increment(self, amount):
        self.amount += amount

    def deduct(self, amount):
        self.amount -= amount

    def update_roll(self, dice_roll):
        self.previous_rolls = self.previous_rolls[-1], dice_roll

    def update_position(self, new_position):
        self.position = new_position

    def double_roll(self):
        return self.previous_rolls[-1][0] == self.previous_rolls[-1][1]

    def debt(self):
        return self._debt['bank'] + self._debt['opponents']

    def add_debt(self, bank=None, opponents=None):
        self._debt['bank'] += bank if bank is not None else 0
        self._debt['opponents'] += opponents if opponents is not None else 0

    def deduct_debt(self, bank=None, opponents=None):
        self._debt['bank'] -= bank if bank is not None else 0
        self._debt['opponents'] -= opponents if opponents is not None else 0

    def __repr__(self):
        repr_str = 'ID: {}\n'.format(self.id)
        repr_str += 'Amount : {}\n'.format(self.amount)
        repr_str += 'Currently at : {}\n'.format(self.position)
        return repr_str
