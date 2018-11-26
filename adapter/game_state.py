from game_state.property_type import PropertyType


def parse(game_context):
    """
    1. Turn Number: int
    2. 42 tuple: properties status, chance-get-out-jail: 41, community-chest-get-out-jail: 42
    3. positions of 2 players: 2 tuples
    4. Player cash: (p1, p2)
    5. current phase: TBD
    6. additional info based on point 5
    7. Debt: 4 len tuple
    8. list of past states: [item1, item2, ..], item1: (agent_id: current player, game_state)
    """

    game_state = game_context.state
    board = game_state.board
    player_1, player_2 = game_state.players

    turn_number = game_state.turn_number
    properties_42_tuple = properties_tuple(board._squares, player_1)
    players_cash = player_1.amount, player_2.amount
    player_1_position = board._reverse_index[player_1.position]
    player_2_position = board._reverse_index[player_2.position]
    player_positions = player_1_position, player_2_position
    current_phase = str(game_context.phase)
    current_phase_details = None
    debt = player_1.debt[0], player_1.debt[1], player_2.debt[0], player_2.debt[1]
    past_states = []
    return turn_number, properties_42_tuple, players_cash, player_positions, current_phase, current_phase_details, debt, past_states


def properties_tuple(properties, player_1):
    def property_mapper(property_):
        if property_.type is PropertyType.UNOWNED:
            return 0
        elif property_.type is PropertyType.JAIL_CHANCE or property_.type is PropertyType.JAIL_COMMUNITY_CHEST:
            if property_.owned_by is None:
                return 0
            else:
                return 1 if property_.owned_by is player_1 else 0
        elif property_.type is PropertyType.COMMUNITY_CHEST or property_.type is PropertyType.CHANCE:
            if property_.owned_by is None:
                return 0
            else:
                return 1 if property_.owned_by is player_1 else 0
        elif property_.type is PropertyType.MORTGAGED:
            return 7 if property_.owned_by is player_1 else -7
        elif property_.owned_by is player_1:
            return property_.houses + 1
        else:
            return -(property_.houses + 1)

    ordered_properties = list(map(lambda i: properties[i], range(42)))
    return tuple(map(property_mapper, ordered_properties))
