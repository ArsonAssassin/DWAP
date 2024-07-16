from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region
from .Items import DigimonWorldItem

class DigimonWorldLocationCategory(IntEnum):
    RECRUIT = 0
    MISC = 1
    EVENT = 2
    SKIP = 3,
    PROSPERITY = 4


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
        base_id = 690000
        table_offset = 1000

        table_order = [
            "Recruitment", "Consumable", "Misc", "Prosperity"
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
        DigimonWorldLocationData("Vegiemon",                             "Vegiemon",                         DigimonWorldLocationCategory.RECRUIT),
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
    "Consumable":
    [
    ],
    "Misc": 
    [           
    ],
    "Prosperity":
    [
        DigimonWorldLocationData("1 Prosperity",                        "SM Recovery",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("2 Prosperity",                       "SM Recovery",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("3 Prosperity",                        "SM Recovery",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("4 Prosperity",                       "SM Recovery",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("5 Prosperity",                        "SM Recovery",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("6 Prosperity",                       "SM Recovery",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("7 Prosperity",                        "SM Recovery",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("8 Prosperity",                       "Various",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("9 Prosperity",                        "Various",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("10 Prosperity",                       "Bandage",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("11 Prosperity",                        "Bandage",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("12 Prosperity",                       "Medicine",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("13 Prosperity",                        "Medicine",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("14 Prosperity",                       "Medicine",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("15 Prosperity",                        "Torn tatter",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("16 Prosperity",                       "Koga laws",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("17 Prosperity",                        "Grey Claws",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("18 Prosperity",                       "SM Recovery",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("19 Prosperity",                        "SM Recovery",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("20 Prosperity",                       "SM Recovery",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("21 Prosperity",                        "SM Recovery",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("22 Prosperity",                       "SM Recovery",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("23 Prosperity",                        "Med Recovery",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("24 Prosperity",                       "Med Recovery",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("25 Prosperity",                        "Med Recovery",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("26 Prosperity",                       "Med Recovery",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("27 Prosperity",                        "Med Recovery",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("28 Prosperity",                       "Med Recovery",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("29 Prosperity",                        "Med Recovery",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("30 Prosperity",                       "Med Recovery",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("31 Prosperity",                        "Lrg Recovery",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("32 Prosperity",                       "Lrg Recovery",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("33 Prosperity",                        "Lrg Recovery",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("34 Prosperity",                       "Lrg Recovery",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("35 Prosperity",                        "Sup Recovery",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("36 Prosperity",                       "Sup Recovery",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("37 Prosperity",                        "Double flop",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("38 Prosperity",                       "Double flop",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("39 Prosperity",                        "Double flop",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("40 Prosperity",                       "Large MP",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("41 Prosperity",                        "Large MP",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("42 Prosperity",                       "Medium MP",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("43 Prosperity",                        "Medium MP",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("44 Prosperity",                       "Medium MP",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("45 Prosperity",                        "Sup.restore",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("46 Prosperity",                       "Sup.restore",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("47 Prosperity",                        "Restore",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("48 Prosperity",                       "Restore",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("49 Prosperity",                        "Health shoe",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("50 Prosperity",                        "Port. potty",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("51 Prosperity",                       "Port. potty",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("52 Prosperity",                        "Port. potty",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("53 Prosperity",                       "Port. potty",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("54 Prosperity",                        "Auto Pilot",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("55 Prosperity",                       "Auto Pilot",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("56 Prosperity",                        "Auto Pilot",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("57 Prosperity",                       "Auto Pilot",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("58 Prosperity",                        "1000 Bits",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("59 Prosperity",                       "1000 Bits",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("60 Prosperity",                        "1000 Bits",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("61 Prosperity",                       "1000 Bits",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("62 Prosperity",                        "1000 Bits",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("63 Prosperity",                       "1000 Bits",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("64 Prosperity",                        "1000 Bits",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("65 Prosperity",                       "1000 Bits",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("66 Prosperity",                        "1000 Bits",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("67 Prosperity",                       "1000 Bits",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("68 Prosperity",                        "1000 Bits",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("69 Prosperity",                       "1000 Bits",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("70 Prosperity",                        "1000 Bits",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("71 Prosperity",                       "1000 Bits",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("72 Prosperity",                        "1000 Bits",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("73 Prosperity",                       "1000 Bits",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("74 Prosperity",                        "5000 Bits",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("75 Prosperity",                       "5000 Bits",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("76 Prosperity",                        "5000 Bits",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("77 Prosperity",                       "5000 Bits",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("78 Prosperity",                        "5000 Bits",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("79 Prosperity",                       "5000 Bits",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("80 Prosperity",                        "5000 Bits",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("81 Prosperity",                       "Progressive Stat Cap",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("82 Prosperity",                        "Progressive Stat Cap",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("83 Prosperity",                       "Progressive Stat Cap",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("84 Prosperity",                       "Progressive Stat Cap",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("85 Prosperity",                        "Progressive Stat Cap",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("86 Prosperity",                       "Progressive Stat Cap",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("87 Prosperity",                        "Progressive Stat Cap",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("88 Prosperity",                       "Progressive Stat Cap",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("89 Prosperity",                        "Progressive Stat Cap",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("90 Prosperity",                       "Black trout",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("91 Prosperity",                       "Black trout",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("92 Prosperity",                        "Chain melon",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("93 Prosperity",                       "Digiseabass",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("94 Prosperity",                       "Digiseabass",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("95 Prosperity",                        "Digiseabass",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("96 Prosperity",                       "Digiseabass",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("97 Prosperity",                        "Rain Plant",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("98 Prosperity",                       "Rain Plant",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("99 Prosperity",                        "Rain Plant",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("100 Prosperity",                       "Rain Plant",                   DigimonWorldLocationCategory.EVENT),
    ]
}

location_dictionary: Dict[str, DigimonWorldLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
