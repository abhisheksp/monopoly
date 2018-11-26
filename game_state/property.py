from game_state.property_type import PropertyType


class Property:
    def __init__(self, name, color, cost, type_, houses=0, build_costs=None, mortgage_value=0, rent=None, group=None,
                 player=None):
        self.name = name
        self.color = color
        self.cost = cost
        self.owned_by = player
        self.type = type_
        self.group = group or []
        self._rent = rent or {}
        self.build_costs = build_costs or {}
        self.houses = houses
        self.mortgage_value = cost * 0.5 if cost else mortgage_value

    def own(self, player):
        self.owned_by = player
        self.type = PropertyType.OWNED

    def build(self, count):
        self.houses += count

    def sell_buildings(self, count):
        self.houses -= count

    def rent(self):
        result = self._rent[self.houses]
        group_owned = all(map(lambda property_: self.owned_by is property_.owned_by, self.group))
        if self.houses == 0 and self.group and group_owned:
            result = self._rent[self.houses] * 2
        return result

    def mortgage(self):
        self.type = PropertyType.MORTGAGED

    def unmortgage(self):
        self.type = PropertyType.OWNED

    def __repr__(self):
        return '{}'.format(self.name)
