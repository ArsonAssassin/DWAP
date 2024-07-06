from enum import IntEnum
from typing import NamedTuple

from BaseClasses import Item


class DigimonWorldItemCategory(IntEnum):
    CONSUMABLE = 0
    MISC = 1,
    EVENT = 2,
    RECRUIT = 3,
    SKIP = 4


class DigimonWorldItemData(NamedTuple):
    name: str
    dw_code: int
    category: DigimonWorldItemCategory


class DigimonWorldItem(Item):
    game: str = "Digimon World"

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 690000
        return {item_data.name: base_id + item_data.dw_code for item_data in _all_items}


key_item_names = {
}


_all_items = [DigimonWorldItemData(row[0], row[1], row[2]) for row in [    
    ("Agumon",             1000, DigimonWorldItemCategory.RECRUIT),  
    ("Betamon",            1001, DigimonWorldItemCategory.RECRUIT),  
    ("Greymon",            1002, DigimonWorldItemCategory.RECRUIT),  
    ("Devimon",            1003, DigimonWorldItemCategory.RECRUIT),  
    ("Airdramon",            1004, DigimonWorldItemCategory.RECRUIT),  
    ("Tyrannomon",            1005, DigimonWorldItemCategory.RECRUIT),  
    ("Meramon",            1006, DigimonWorldItemCategory.RECRUIT),  
    ("Seadramon",            1007, DigimonWorldItemCategory.RECRUIT),  
    ("Numemon",            1008, DigimonWorldItemCategory.RECRUIT),  
    ("MetalGreymon",            1009, DigimonWorldItemCategory.RECRUIT),  
    ("Mamemon",            1010, DigimonWorldItemCategory.RECRUIT),  
    ("Monzaemon",            1011, DigimonWorldItemCategory.RECRUIT),  
    ("Gabumon",            1012, DigimonWorldItemCategory.RECRUIT),  
    ("Elecmon",            1013, DigimonWorldItemCategory.RECRUIT),  
    ("Kabuterimon",            1014, DigimonWorldItemCategory.RECRUIT),  
    ("Angemon",            1015, DigimonWorldItemCategory.RECRUIT),  
    ("Birdramon",            1016, DigimonWorldItemCategory.RECRUIT),  
    ("Garurumon",            1017, DigimonWorldItemCategory.RECRUIT),  
    ("Frigimon",            1018, DigimonWorldItemCategory.RECRUIT),  
    ("Whamon",            1019, DigimonWorldItemCategory.RECRUIT),  
    ("Vegiemon",            1020, DigimonWorldItemCategory.RECRUIT),  
    ("SkullGreymon",            1021, DigimonWorldItemCategory.RECRUIT),  
    ("MetalMamemon",            1022, DigimonWorldItemCategory.RECRUIT),  
    ("Vademon",            1023, DigimonWorldItemCategory.RECRUIT),  
    ("Patamon",            1024, DigimonWorldItemCategory.RECRUIT),  
    ("Kunemon",            1025, DigimonWorldItemCategory.RECRUIT),  
    ("Unimon",            1026, DigimonWorldItemCategory.RECRUIT),  
    ("Ogremon",            1027, DigimonWorldItemCategory.RECRUIT),  
    ("Shellmon",            1028, DigimonWorldItemCategory.RECRUIT),  
    ("Centarumon",            1029, DigimonWorldItemCategory.RECRUIT),  
    ("Bakemon",            1030, DigimonWorldItemCategory.RECRUIT),  
    ("Drimogemon",            1031, DigimonWorldItemCategory.RECRUIT),  
    ("Sukamon",            1032, DigimonWorldItemCategory.RECRUIT),  
    ("Andromon",            1033, DigimonWorldItemCategory.RECRUIT),  
    ("Giromon",            1034, DigimonWorldItemCategory.RECRUIT),  
    ("Etemon",            1035, DigimonWorldItemCategory.RECRUIT),  
    ("Biyomon",            1036, DigimonWorldItemCategory.RECRUIT),  
    ("Palmon",            1037, DigimonWorldItemCategory.RECRUIT),  
    ("Monochromon",            1038, DigimonWorldItemCategory.RECRUIT),  
    ("Leomon",            1039, DigimonWorldItemCategory.RECRUIT),  
    ("Coelamon",            1040, DigimonWorldItemCategory.RECRUIT),  
    ("Kokatorimon",            1041, DigimonWorldItemCategory.RECRUIT),  
    ("Kuwagamon",            1042, DigimonWorldItemCategory.RECRUIT),  
    ("Mojyamon",            1043, DigimonWorldItemCategory.RECRUIT),  
    ("Nanimon",            1044, DigimonWorldItemCategory.RECRUIT),  
    ("Megadramon",            1045, DigimonWorldItemCategory.RECRUIT),  
    ("Piximon",            1046, DigimonWorldItemCategory.RECRUIT),  
    ("Digitamamon",            1047, DigimonWorldItemCategory.RECRUIT),  
    ("Penguinmon",            1048, DigimonWorldItemCategory.RECRUIT),  
    ("Ninjamon",            1049, DigimonWorldItemCategory.RECRUIT),  
    
    ("SM Recovery",            2000, DigimonWorldItemCategory.CONSUMABLE),  
    ("1000 Bits",            2001, DigimonWorldItemCategory.MISC),      
    
    #("Bridge Fixed",            3001, DigimonWorldItemCategory.EVENT),  
]]

item_descriptions = {
}

item_dictionary = {item_data.name: item_data for item_data in _all_items}
