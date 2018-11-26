from enum import Enum, auto


class PropertyType(Enum):
    UNOWNED = auto()
    OWNED = auto()
    MORTGAGED = auto()
    GO = auto()
    CHANCE = auto()
    COMMUNITY_CHEST = auto()
    INCOME_TAX = auto()
    JAIL_CHANCE = auto()
    JAIL_COMMUNITY_CHEST = auto()
