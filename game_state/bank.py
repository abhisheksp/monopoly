class Bank:
    def __init__(self, houses=32, hotels=12):
        self.houses = houses
        self.hotels = hotels

    def houses_available(self):
        return self.houses > 0
