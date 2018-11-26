import adapter.game_state
from utils.context_factory import context_factory


class Adjudicator:
    @staticmethod
    def runGame(player_1, player_2, dice_rolls=None, chance_cards=None, community_chest_cards=None):
        count = 0
        context = context_factory(player_1, player_2, dice_rolls)
        action = None
        while count < len(dice_rolls):
            context, action = context.apply(action)
            print(context.phase)
            print(context.state)
            if str(context.phase) == 'Turn End Phase':
                count += 1
        return None, adapter.game_state.parse(context)
