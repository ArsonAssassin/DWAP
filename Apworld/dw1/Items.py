from enum import IntEnum
from typing import NamedTuple
import random
from BaseClasses import Item


class DigimonWorldItemCategory(IntEnum):
    CONSUMABLE = 0
    MISC = 1,
    EVENT = 2,
    RECRUIT = 3,
    SKIP = 4,
    DV = 5


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
    #"Progressive Stat Cap"
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
    ("Med Recovery",           2001, DigimonWorldItemCategory.CONSUMABLE),
    ("Lrg Recovery",           2002, DigimonWorldItemCategory.CONSUMABLE),
    ("Sup Recovery",           2003, DigimonWorldItemCategory.CONSUMABLE),
    ("MP Floppy",              2004, DigimonWorldItemCategory.CONSUMABLE),
    ("Medium MP",              2005, DigimonWorldItemCategory.CONSUMABLE),
    ("Large MP",               2006, DigimonWorldItemCategory.CONSUMABLE),
    ("Double flop",            2007, DigimonWorldItemCategory.CONSUMABLE),
    ("Various",                2008, DigimonWorldItemCategory.CONSUMABLE),
    ("Omnipotent",             2009, DigimonWorldItemCategory.CONSUMABLE),
    ("Protection",             2010, DigimonWorldItemCategory.CONSUMABLE),
    ("Restore",                2011, DigimonWorldItemCategory.CONSUMABLE),
    ("Sup.restore",            2012, DigimonWorldItemCategory.CONSUMABLE),
    ("Bandage",                2013, DigimonWorldItemCategory.CONSUMABLE),
    ("Medicine",               2014, DigimonWorldItemCategory.CONSUMABLE),
    ("Off. Disk",              2015, DigimonWorldItemCategory.CONSUMABLE),
    ("Def. Disk",              2016, DigimonWorldItemCategory.CONSUMABLE),
    ("Hispeed dsk",            2017, DigimonWorldItemCategory.CONSUMABLE),
    ("Omni Disk",              2018, DigimonWorldItemCategory.CONSUMABLE),
    ("S.Off.disk",             2019, DigimonWorldItemCategory.CONSUMABLE),
    ("S.Def.disk",             2020, DigimonWorldItemCategory.CONSUMABLE),
    ("S.speed.disk",           2021, DigimonWorldItemCategory.CONSUMABLE),
    ("Auto Pilot",             2022, DigimonWorldItemCategory.CONSUMABLE),
    ("Off. Chip",              2023, DigimonWorldItemCategory.CONSUMABLE),
    ("Def. Chip",              2024, DigimonWorldItemCategory.CONSUMABLE),
    ("Brain Chip",             2025, DigimonWorldItemCategory.CONSUMABLE),
    ("Quick Chip",             2026, DigimonWorldItemCategory.CONSUMABLE),
    ("HP Chip",                2027, DigimonWorldItemCategory.CONSUMABLE),
    ("MP Chip",                2028, DigimonWorldItemCategory.CONSUMABLE),
    ("DV Chip A",              2029, DigimonWorldItemCategory.CONSUMABLE),
    ("DV Chip D",              2030, DigimonWorldItemCategory.CONSUMABLE),
    ("DV Chip E",              2031, DigimonWorldItemCategory.CONSUMABLE),
    ("Port. potty",            2032, DigimonWorldItemCategory.CONSUMABLE),
    ("Trn. manual",            2033, DigimonWorldItemCategory.MISC),
    ("Rest pillow",            2034, DigimonWorldItemCategory.MISC),
    ("Enemy repel",            2035, DigimonWorldItemCategory.MISC),
    ("Enemy bell",             2036, DigimonWorldItemCategory.MISC),
    ("Health shoe",            2037, DigimonWorldItemCategory.MISC),
    ("Meat",                   2038, DigimonWorldItemCategory.CONSUMABLE),
    ("Giant Meat",             2039, DigimonWorldItemCategory.CONSUMABLE),
    ("Sirloin",                2040, DigimonWorldItemCategory.CONSUMABLE),
    ("Supercarrot",            2041, DigimonWorldItemCategory.CONSUMABLE),
    ("Hawk radish",            2042, DigimonWorldItemCategory.CONSUMABLE),
    ("Spiny green",            2043, DigimonWorldItemCategory.CONSUMABLE),
    ("Digimushrm",             2044, DigimonWorldItemCategory.CONSUMABLE),
    ("Ice mushrm",             2045, DigimonWorldItemCategory.CONSUMABLE),
    ("Deluxmushrm",            2046, DigimonWorldItemCategory.CONSUMABLE),
    ("Digipine",               2047, DigimonWorldItemCategory.CONSUMABLE),
    ("Blue apple",             2048, DigimonWorldItemCategory.CONSUMABLE),
    ("Red Berry",              2049, DigimonWorldItemCategory.CONSUMABLE),
    ("Gold Acorn",             2050, DigimonWorldItemCategory.CONSUMABLE),
    ("Big Berry",              2051, DigimonWorldItemCategory.CONSUMABLE),
    ("Sweet Nut",              2052, DigimonWorldItemCategory.CONSUMABLE),
    ("Super veggy",            2053, DigimonWorldItemCategory.CONSUMABLE),
    ("Pricklypear",            2054, DigimonWorldItemCategory.CONSUMABLE),
    ("Orange bana",            2055, DigimonWorldItemCategory.CONSUMABLE),
    ("Power fruit",            2056, DigimonWorldItemCategory.CONSUMABLE),
    ("Power Ice",              2057, DigimonWorldItemCategory.CONSUMABLE),
    ("Speed Leaf",             2058, DigimonWorldItemCategory.CONSUMABLE),
    ("Sage Fruit",             2059, DigimonWorldItemCategory.CONSUMABLE),
    ("Muscle Yam",             2060, DigimonWorldItemCategory.CONSUMABLE),
    ("Calm berry",             2061, DigimonWorldItemCategory.CONSUMABLE),
    ("Digianchovy",            2062, DigimonWorldItemCategory.CONSUMABLE),
    ("Digisnapper",            2063, DigimonWorldItemCategory.CONSUMABLE),
    ("DigiTrout",              2064, DigimonWorldItemCategory.CONSUMABLE),
    ("Black trout",            2065, DigimonWorldItemCategory.CONSUMABLE),
    ("Digicatfish",            2066, DigimonWorldItemCategory.CONSUMABLE),
    ("Digiseabass",            2067, DigimonWorldItemCategory.CONSUMABLE),
    ("Moldy Meat",             2068, DigimonWorldItemCategory.CONSUMABLE),
    ("Happymushrm",            2069, DigimonWorldItemCategory.CONSUMABLE),
    ("Chain melon",            2070, DigimonWorldItemCategory.CONSUMABLE),
    ("Grey Claws",             2071, DigimonWorldItemCategory.DV),
    ("Fireball",               2072, DigimonWorldItemCategory.DV),
    ("Flamingwing",            2073, DigimonWorldItemCategory.DV),
    ("Iron Hoof",              2074, DigimonWorldItemCategory.DV),
    ("Mono Stone",             2075, DigimonWorldItemCategory.DV),
    ("Steel drill",            2076, DigimonWorldItemCategory.DV),
    ("White Fang",             2077, DigimonWorldItemCategory.DV),
    ("Black Wing",             2078, DigimonWorldItemCategory.DV),
    ("Spike Club",             2079, DigimonWorldItemCategory.DV),
    ("Flamingmane",            2080, DigimonWorldItemCategory.DV),
    ("White Wing",             2081, DigimonWorldItemCategory.DV),
    ("Torn tatter",            2082, DigimonWorldItemCategory.DV),
    ("Electo ring",            2083, DigimonWorldItemCategory.DV),
    ("Rainbowhorn",            2084, DigimonWorldItemCategory.DV),
    ("Rooster",                2085, DigimonWorldItemCategory.DV),
    ("Unihorn",                2086, DigimonWorldItemCategory.DV),
    ("Horn helmet",            2087, DigimonWorldItemCategory.DV),
    ("Scissor jaw",            2088, DigimonWorldItemCategory.DV),
    ("Fertilizer",             2089, DigimonWorldItemCategory.DV),
    ("Koga laws",              2090, DigimonWorldItemCategory.DV),
    ("Waterbottle",            2091, DigimonWorldItemCategory.DV),
    ("North Star",             2092, DigimonWorldItemCategory.DV),
    ("Red Shell",              2093, DigimonWorldItemCategory.DV),
    ("Hard Scale",             2094, DigimonWorldItemCategory.DV),
    ("Bluecrystal",            2095, DigimonWorldItemCategory.DV),
    ("Ice crystal",            2096, DigimonWorldItemCategory.DV),
    ("Hair grower",            2097, DigimonWorldItemCategory.DV),
    ("Sunglasses",             2098, DigimonWorldItemCategory.DV),
    ("Metal part",             2099, DigimonWorldItemCategory.DV),
    ("Fatal Bone",             2100, DigimonWorldItemCategory.DV),
    ("Cyber part",             2101, DigimonWorldItemCategory.DV),
    ("Mega Hand",              2102, DigimonWorldItemCategory.DV),
    ("Silver ball",            2103, DigimonWorldItemCategory.DV),
    ("Metal armor",            2104, DigimonWorldItemCategory.DV),
    ("Chainsaw",               2105, DigimonWorldItemCategory.DV),
    ("Small spear",            2106, DigimonWorldItemCategory.DV),
    ("X Bandage",              2107, DigimonWorldItemCategory.DV),
    ("Ray Gun",                2108, DigimonWorldItemCategory.DV),
    ("Gold banana",            2109, DigimonWorldItemCategory.DV),
    ("Mysty Egg",              2110, DigimonWorldItemCategory.DV),
    ("Red Ruby",               2111, DigimonWorldItemCategory.DV),
    ("Beetlepearl",            2112, DigimonWorldItemCategory.DV),
    ("Coral charm",            2113, DigimonWorldItemCategory.DV),
    ("Moon mirror",            2114, DigimonWorldItemCategory.DV),
    ("Blue Flute",             2115, DigimonWorldItemCategory.MISC),
    ("old fishrod",            2116, DigimonWorldItemCategory.MISC),
    ("Amazing rod",            2117, DigimonWorldItemCategory.MISC),
    ("Leomonstone",            2118, DigimonWorldItemCategory.MISC),
    ("Mansion key",            2119, DigimonWorldItemCategory.MISC),
    ("Gear",                   2120, DigimonWorldItemCategory.MISC),
    ("Rain Plant",             2121, DigimonWorldItemCategory.CONSUMABLE),
    ("Steak",                  2122, DigimonWorldItemCategory.CONSUMABLE),
    ("Frig Key",               2123, DigimonWorldItemCategory.MISC),
    ("AS Decoder",             2124, DigimonWorldItemCategory.MISC),
    ("Giga Hand",              2125, DigimonWorldItemCategory.DV),
    ("Noble Mane",             2126, DigimonWorldItemCategory.DV),
    ("Metalbanana",            2127, DigimonWorldItemCategory.DV),  
    
    ("Progressive Stat Cap",            3000, DigimonWorldItemCategory.MISC),  
    ("1000 Bits",            3001, DigimonWorldItemCategory.MISC),      
    ("5000 Bits",            3002, DigimonWorldItemCategory.MISC),      
    #("Bridge Fixed",            3001, DigimonWorldItemCategory.EVENT),  
]]

item_descriptions = {
}

item_dictionary = {item_data.name: item_data for item_data in _all_items}

def BuildItemPool(count, includeProgressive, guaranteed_items):
    item_pool = []

    consumable_count = round(count * 0.6)
    dv_count = random.randint(1, 10)
    bit_count = count - (consumable_count + dv_count)

    if guaranteed_items:
        for item_name in guaranteed_items:
            item = item_dictionary[item_name]
            item_pool.append(item)
            bit_count -= 1
    if(includeProgressive):
        # add 9 stat cap items to the pool
        for i in range(9):
            item_pool.append(item_dictionary["Progressive Stat Cap"])
            bit_count -= 1

    for i in range(consumable_count):
        consumables = [item for item in _all_items if item.category == DigimonWorldItemCategory.CONSUMABLE]
        item = random.choice(consumables)
        item_pool.append(item)
    for i in range(dv_count):
        dv = [item for item in _all_items if item.category == DigimonWorldItemCategory.DV]
        item = random.choice(dv)
        item_pool.append(item)
    for i in range(bit_count):    
        bit = [item for item in _all_items if "Bits" in item.name]
        item = random.choice(bit)
        item_pool.append(item)    
    random.shuffle(item_pool)
    return item_pool
