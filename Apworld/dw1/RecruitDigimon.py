from typing import NamedTuple

class RecruitDigimon(NamedTuple):
    name: str
    prosperity_value: int
    digimon_requirements: list
    prosperity_requirement: int
    

recruit_digimon_list = [RecruitDigimon(row[0], row[1], row[2], row[3]) for row in 
[
    ("Agumon",             1, [], 0),
    ("Gabumon",            1, ["Agumon"], 1),
    ("Patamon",            1, ["Agumon"], 1),
    ("Biyomon",            1, ["Agumon"], 1),
    ("Elecmon",            1, ["Agumon"], 1),
    ("Kunemon",            1, ["Agumon"], 1),
    ("Palmon",             1, ["Agumon"], 1),
    ("Betamon",            1, ["Agumon"], 1),
    ("Penguinmon",         1, ["Agumon"], 1),
    ("Greymon",            2, ["Agumon"], 15),
    ("Monochromon",        2, ["Agumon"], 1),
    ("Ogremon",            2, ["Agumon"], 6),
    ("Airdramon",          2, ["Agumon"], 50),
    ("Kuwagamon",          2, ["Agumon","Seadramon"], 1),
    ("Whamon",             2, ["Agumon"], 1),
    ("Frigimon",           2, ["Agumon"], 1),
    ("Nanimon",            1, ["Agumon", "Leomon", "Tyrannomon", "Numemon"], 1),
    ("Meramon",            2, ["Agumon"], 1),
    ("Drimogemon",         2, ["Agumon"], 1),
    ("Leomon",             2, ["Agumon"], 50),
    ("Kokatorimon",        2, ["Agumon"], 1),
    ("Vegiemon",           2, ["Agumon", "Palmon"], 1),
    ("Shellmon",           2, ["Agumon"], 1),
    ("Mojyamon",           2, ["Agumon"], 1),
    ("Birdramon",          2, ["Agumon"], 1),
    ("Tyrannomon",         2, ["Agumon","Centarumon"], 1),
    ("Angemon",            2, ["Agumon"], 1),
    ("Unimon",             2, ["Agumon","Centarumon"], 1),
    ("Ninjamon",           2, ["Agumon"], 50),
    ("Coelamon",           2, ["Agumon"], 1),
    ("Numemon",            1, ["Agumon","Whamon"], 1),
    ("Centarumon",         2, ["Agumon"], 1),
    ("Devimon",            2, ["Agumon"], 50),
    ("Bakemon",            2, ["Agumon"], 1),
    ("Kabuterimon",        2, ["Agumon","Seadramon"], 1),
    ("Seadramon",          2, ["Agumon"], 1),
    ("Garurumon",          2, ["Agumon"], 1),
    ("Sukamon",            1, ["Agumon"], 1),
    ("MetalGreymon",       3, ["Agumon","Greymon"], 50),
    ("SkullGreymon",       3, ["Agumon","Greymon"], 50),
    ("Mamemon",            3, ["Agumon"], 1),
    ("Giromon",            3, ["Agumon","Numemon"], 1),
    ("Monzaemon",          3, ["Agumon"], 1),
    ("Andromon",           3, ["Agumon", "Numemon"], 1),
    ("Etemon",             3, ["Agumon"], 50),
    ("Digitamamon",        3, ["Agumon","MetalGreymon"], 50),
    ("MetalMamemon",       3, ["Agumon"], 1),
    ("Vademon",            3, ["Agumon","Shellmon"], 45),
    ("Megadramon",         3, ["Agumon"], 50),
    ("Piximon",            3, ["Agumon"], 1),
]]

