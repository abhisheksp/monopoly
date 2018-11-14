from random import seed, randint


class Dice:
    def __init__(self):
        seed(6690106822)

    def roll(self):
        roll_1 = randint(1, 6)
        roll_2 = randint(1, 6)
        return roll_1, roll_2
