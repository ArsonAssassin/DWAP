from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region
from .Items import DigimonWorldItem

class DigimonWorldLocationCategory(IntEnum):
    RECRUIT = 0
    MISC = 1
    EVENT = 2
    SKIP = 3


class DigimonWorldLocationData(NamedTuple):
    name: str
    default_item: str
    category: DigimonWorldLocationCategory


class DigimonWorldLocation(Location):
    game: str = "Digimon World"
    category: DigimonWorldLocationCategory
    default_item_name: str

    def __init__(
            self,
            player: int,
            name: str,
            category: DigimonWorldLocationCategory,
            default_item_name: str,
            address: Optional[int] = None,
            parent: Optional[Region] = None):
        super().__init__(player, name, address, parent)
        self.default_item_name = default_item_name
        self.category = category

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 691000
        table_offset = 1000

        table_order = [
            "Recruitment", "Misc"
        ]

        output = {}
        for i, region_name in enumerate(table_order):
            if len(location_tables[region_name]) > table_offset:
                raise Exception("A location table has {} entries, that is more than {} entries (table #{})".format(len(location_tables[region_name]), table_offset, i))

            output.update({location_data.name: id for id, location_data in enumerate(location_tables[region_name], base_id + (table_offset * i))})

        return output

    def place_locked_item(self, item: DigimonWorldItem):
        self.item = item
        self.locked = True
        item.location = self

location_tables = {
    "Recruitment": [
        DigimonWorldLocationData("Agumon",                               "Agumon",                           DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Betamon",                              "Betamon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Greymon",                              "Greymon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Devimon",                              "Devimon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Airdramon",                            "Airdramon",                        DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Tyrannomon",                           "Tyrannomon",                       DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Meramon",                              "Meramon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Seadramon",                            "Seadramon",                        DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Numemon",                              "Numemon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("MetalGreymon",                         "MetalGreymon",                     DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Mamemon",                              "Mamemon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Monzaemon",                            "Monzaemon",                        DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Gabumon",                              "Gabumon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Elecmon",                              "Elecmon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Kabuterimon",                          "Kabuterimon",                      DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Angemon",                              "Angemon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Birdramon",                            "Birdramon",                        DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Garurumon",                            "Garurumon",                        DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Frigimon",                             "Frigimon",                         DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Whamon",                               "Whamon",                           DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Vegimon",                              "Vegimon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("SkullGreymon",                         "SkullGreymon",                     DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("MetalMamemon",                         "MetalMamemon",                     DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Vademon",                              "Vademon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Patamon",                              "Patamon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Kunemon",                              "Kunemon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Unimon",                               "Unimon",                           DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Ogremon",                              "Ogremon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Shellmon",                             "Shellmon",                         DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Centarumon",                           "Centarumon",                       DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Bakemon",                              "Bakemon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Drimogemon",                           "Drimogemon",                       DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Sukamon",                              "Sukamon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Andromon",                             "Andromon",                         DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Giromon",                              "Giromon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Etemon",                               "Etemon",                           DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Biyomon",                              "Biyomon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Palmon",                               "Palmon",                           DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Monochromon",                          "Monochromon",                      DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Leomon",                               "Leomon",                           DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Coelamon",                             "Coelamon",                         DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Kokatorimon",                          "Kokatorimon",                      DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Kuwagamon",                            "Kuwagamon",                        DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Mojyamon",                             "Mojyamon",                         DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Nanimon",                              "Nanimon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Megadramon",                           "Megadramon",                       DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Piximon",                              "Piximon",                          DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Digitamamon",                          "Digitamamon",                      DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Penguinmon",                           "Penguinmon",                       DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Ninjamon",                             "Ninjamon",                         DigimonWorldLocationCategory.RECRUIT),
    ],
    "Misc": 
    [    
        DigimonWorldLocationData("50 Prosperity",                        "50 Prosperity",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("100 Prosperity",                       "100 Prosperity",                   DigimonWorldLocationCategory.EVENT),
    ]
}

location_dictionary: Dict[str, DigimonWorldLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
