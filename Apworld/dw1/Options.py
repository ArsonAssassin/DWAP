import typing

from Options import Toggle, DefaultOnToggle, Option, Range, Choice, ItemDict, DeathLink


class GuaranteedItemsOption(ItemDict):
    """Guarantees that the specified items will be in the item pool"""
    display_name = "Guaranteed Items"

class ExpMultiplierOption(Range):
    """Multiplies stat gain by specified amount"""
    display_name = "Exp Multiplier"
    min_value = 1
    range_start = 1
    range_end = 10
    default = 1

class ProgressiveStatOption(DefaultOnToggle):
    """Enables Progressive Stat gain caps"""
    display_name = "Progressive Stat Caps"

class RandomStarterOption(Choice):
    """Randomise the 2 starter digimon options
    Vanilla = Agumon and Gabumon are the starters
    All = Any digimon can be a starter
    Rookie = Only rookie digimon can be a starter"""
    display_name = "Random starter digimon"
    option_vanilla = 0
    option_all = 1
    option_rookie = 2

digimon_world_options: typing.Dict[str, Option] = {

    "guaranteed_items": GuaranteedItemsOption,
    "exp_multiplier": ExpMultiplierOption,
    "progressive_stats": ProgressiveStatOption,
    "random_starter": RandomStarterOption,
}
