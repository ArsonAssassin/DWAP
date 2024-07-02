import typing

from Options import Toggle, DefaultOnToggle, Option, Range, Choice, ItemDict, DeathLink


class GuaranteedItemsOption(ItemDict):
    """Guarantees that the specified items will be in the item pool"""
    display_name = "Guaranteed Items"

digimon_world_options: typing.Dict[str, Option] = {

    "guaranteed_items": GuaranteedItemsOption,
}
