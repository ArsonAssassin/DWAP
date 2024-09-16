from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region
from .Items import DigimonWorldItem

class DigimonWorldLocationCategory(IntEnum):
    RECRUIT = 0
    MISC = 1
    EVENT = 2
    SKIP = 3,
    PROSPERITY = 4,
    CARD = 5,


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
        base_id = 69000000
        table_offset = 1000

        table_order = [
            "Consumable", "Misc", "Cards", "Start Game", "Prosperity",
            "Agumon", "Betamon","Greymon","Devimon","Airdramon","Tyrannomon","Meramon","Seadramon","Numemon","MetalGreymon","Mamemon","Monzaemon",
            "Gabumon","Elecmon","Kabuterimon","Angemon","Birdramon","Garurumon","Frigimon","Whamon","Vegiemon","SkullGreymon","MetalMamemon","Vademon",
            "Patamon","Kunemon","Unimon","Ogremon","Shellmon","Centarumon","Bakemon","Drimogemon","Sukamon","Andromon", "Giromon", "Etemon", "Biyomon",
            "Palmon", "Monochromon", "Leomon", "Coelamon", "Kokatorimon", "Kuwagamon", "Mojyamon", "Nanimon", "Megadramon", "Piximon", "Digitamamon",
            "Penguinmon", "Ninjamon"
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
    "Start Game": [
        DigimonWorldLocationData("Start Game", "Agumon Soul", DigimonWorldLocationCategory.RECRUIT),
    ],
    "Agumon": [
        DigimonWorldLocationData("Agumon", "1000 Bits", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Agumon Recruited", "Agumon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Betamon": [
        DigimonWorldLocationData("Betamon", "Betamon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Betamon Recruited", "Betamon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Greymon": [
        DigimonWorldLocationData("Greymon", "Greymon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Greymon Recruited", "Greymon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Devimon": [
        DigimonWorldLocationData("Devimon", "Devimon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Devimon Recruited", "Devimon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Airdramon": [
        DigimonWorldLocationData("Airdramon", "Airdramon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Airdramon Recruited", "Airdramon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Tyrannomon": [
        DigimonWorldLocationData("Tyrannomon", "Tyrannomon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Tyrannomon Recruited", "Tyrannomon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Meramon": [
        DigimonWorldLocationData("Meramon", "Meramon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Meramon Recruited", "Meramon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Seadramon": [
        DigimonWorldLocationData("Seadramon", "Seadramon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Seadramon Recruited", "Seadramon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Numemon": [
        DigimonWorldLocationData("Numemon", "Numemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Numemon Recruited", "Numemon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "MetalGreymon": [
        DigimonWorldLocationData("MetalGreymon", "MetalGreymon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("MetalGreymon Recruited", "MetalGreymon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Mamemon": [
        DigimonWorldLocationData("Mamemon", "Mamemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Mamemon Recruited", "Mamemon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Monzaemon": [
        DigimonWorldLocationData("Monzaemon", "Monzaemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Monzaemon Recruited", "Monzaemon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Gabumon": [
        DigimonWorldLocationData("Gabumon", "Gabumon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Gabumon Recruited", "Gabumon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Elecmon": [
        DigimonWorldLocationData("Elecmon", "Elecmon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Elecmon Recruited", "Elecmon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Kabuterimon": [
        DigimonWorldLocationData("Kabuterimon", "Kabuterimon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Kabuterimon Recruited", "Kabuterimon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Angemon": [
        DigimonWorldLocationData("Angemon", "Angemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Angemon Recruited", "Angemon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Birdramon": [
        DigimonWorldLocationData("Birdramon", "Birdramon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Birdramon Recruited", "Birdramon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Garurumon": [
        DigimonWorldLocationData("Garurumon", "Garurumon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Garurumon Recruited", "Garurumon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Frigimon": [
        DigimonWorldLocationData("Frigimon", "Frigimon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Frigimon Recruited", "Frigimon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Whamon": [
        DigimonWorldLocationData("Whamon", "Whamon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Whamon Recruited", "Whamon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Vegiemon": [
        DigimonWorldLocationData("Vegiemon", "Vegiemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Vegiemon Recruited", "Vegiemon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "SkullGreymon": [
        DigimonWorldLocationData("SkullGreymon", "SkullGreymon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("SkullGreymon Recruited", "SkullGreymon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "MetalMamemon": [
        DigimonWorldLocationData("MetalMamemon", "MetalMamemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("MetalMamemon Recruited", "MetalMamemon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Vademon": [
        DigimonWorldLocationData("Vademon", "Vademon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Vademon Recruited", "Vademon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Patamon": [
        DigimonWorldLocationData("Patamon", "Patamon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Patamon Recruited", "Patamon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Kunemon": [
        DigimonWorldLocationData("Kunemon", "Kunemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Kunemon Recruited", "Kunemon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Unimon": [
        DigimonWorldLocationData("Unimon", "Unimon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Unimon Recruited", "Unimon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Ogremon": [
        DigimonWorldLocationData("Ogremon", "Ogremon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Ogremon Recruited", "Ogremon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Shellmon": [
        DigimonWorldLocationData("Shellmon", "Shellmon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Shellmon Recruited", "Shellmon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Centarumon": [
        DigimonWorldLocationData("Centarumon", "Centarumon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Centarumon Recruited", "Centarumon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Bakemon": [
        DigimonWorldLocationData("Bakemon", "Bakemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Bakemon Recruited", "Bakemon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Drimogemon": [
        DigimonWorldLocationData("Drimogemon", "Drimogemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Drimogemon Recruited", "Drimogemon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Sukamon": [
        DigimonWorldLocationData("Sukamon", "Sukamon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Sukamon Recruited", "Sukamon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Andromon": [
        DigimonWorldLocationData("Andromon", "Andromon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Andromon Recruited", "Andromon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Giromon": [
        DigimonWorldLocationData("Giromon", "Giromon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Giromon Recruited", "Giromon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Etemon": [
        DigimonWorldLocationData("Etemon", "Etemon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Etemon Recruited", "Etemon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Biyomon": [
        DigimonWorldLocationData("Biyomon", "Biyomon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Biyomon Recruited", "Biyomon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Palmon": [
        DigimonWorldLocationData("Palmon", "Palmon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Palmon Recruited", "Palmon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Monochromon": [
        DigimonWorldLocationData("Monochromon", "Monochromon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Monochromon Recruited", "Monochromon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Leomon": [
        DigimonWorldLocationData("Leomon", "Leomon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Leomon Recruited", "Leomon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Coelamon": [
        DigimonWorldLocationData("Coelamon", "Coelamon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Coelamon Recruited", "Coelamon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Kokatorimon": [
        DigimonWorldLocationData("Kokatorimon", "Kokatorimon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Kokatorimon Recruited", "Kokatorimon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Kuwagamon": [
        DigimonWorldLocationData("Kuwagamon", "Kuwagamon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Kuwagamon Recruited", "Kuwagamon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Mojyamon": [
        DigimonWorldLocationData("Mojyamon", "Mojyamon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Mojyamon Recruited", "Mojyamon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Nanimon": [
        DigimonWorldLocationData("Nanimon", "Nanimon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Nanimon Recruited", "Nanimon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Megadramon": [
        DigimonWorldLocationData("Megadramon", "Megadramon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Megadramon Recruited", "Megadramon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Piximon": [
        DigimonWorldLocationData("Piximon", "Piximon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Piximon Recruited", "Piximon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Digitamamon": [
        DigimonWorldLocationData("Digitamamon", "Digitamamon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Digitamamon Recruited", "Digitamamon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Penguinmon": [
        DigimonWorldLocationData("Penguinmon", "Penguinmon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Penguinmon Recruited", "Penguinmon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Ninjamon": [
        DigimonWorldLocationData("Ninjamon", "Ninjamon Soul", DigimonWorldLocationCategory.RECRUIT),
        DigimonWorldLocationData("Ninjamon Recruited", "Ninjamon Recruited", DigimonWorldLocationCategory.SKIP),
    ],
    "Item Boxes":[

    ],
    "Cards":[
        DigimonWorldLocationData("Player Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Phoenixmon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("H-Kabuterimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("MegaSeadramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("ShogunGekomon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Myotismon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("MetalGreymon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Mamemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Monzaemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("SkullGreymon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("MetalMamemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Vademon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Andromon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Giromon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Etemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Megadramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Piximon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Digitamamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Gekomon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("WaruMonzaemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Jijimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("King of Sukamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Cherrymon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Guardromon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Hagurumon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Brachiomon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Greymon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Devimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Airdramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Tyrannomon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Meramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Seadramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Kabuterimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Angemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Birdramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Garurumon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Frigimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Whamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Unimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Ogremon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Shellmon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Centarumon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Bakemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Drimogemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Monochromon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Leomon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Coelamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Kokatorimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Kuwagamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Mojyamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Ninjamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Penguinmon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Otamamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Tentomon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Yanmamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Gotsumon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Darkrizamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("ToyAgumon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("DemiMeramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Tankmon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Goburimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Numemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Vegiemon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Sukamon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Nanimon Card", "1000 Bits", DigimonWorldLocationCategory.CARD),
        DigimonWorldLocationData("Machinedramon Card", "1000 Bits", DigimonWorldLocationCategory.CARD), 
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
        DigimonWorldLocationData("81 Prosperity",                       "1000 Bits",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("82 Prosperity",                        "1000 Bits",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("83 Prosperity",                       "1000 Bits",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("84 Prosperity",                       "1000 Bits",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("85 Prosperity",                        "1000 Bits",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("86 Prosperity",                       "1000 Bits",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("87 Prosperity",                        "1000 Bits",                    DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("88 Prosperity",                       "1000 Bits",                   DigimonWorldLocationCategory.EVENT),
        DigimonWorldLocationData("89 Prosperity",                        "1000 Bits",                    DigimonWorldLocationCategory.EVENT),
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
    ],
    "Consumable": [],
    "Misc": [        
    ],
}
location_dictionary: Dict[str, DigimonWorldLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
