from .Locations import DigimonWorldLocation

def get_digimon_prosperity_list(self) -> list:
    digimon_prosperity_points = {
            "Agumon": 1,
            "Gabumon": 1,
            "Patamon": 1,
            "Biyomon": 1,
            "Elecmon": 1,
            "Kunemon": 1,
            "Palmon": 1,
            "Betamon": 1,
            "Penguinmon": 1,
            "Greymon": 2,
            "Monochromon": 2,
            "Ogremon": 2,
            "Airdramon": 2,
            "Kuwagamon": 2,
            "Whamon": 2,
            "Frigimon": 2,
            "Nanimon": 1,
            "Meramon": 2,
            "Drimogemon": 2,
            "Leomon": 2,
            "Kokatorimon": 2,
            "Vegiemon": 2,
            "Shellmon": 2,
            "Mojyamon": 2,
            "Birdramon": 2,
            "Tyrannomon": 2,
            "Angemon": 2,
            "Unimon": 2,
            "Ninjamon": 2,
            "Coelamon": 2,
            "Numemon": 1,
            "Centarumon": 2,
            "Devimon": 2,
            "Bakemon": 2,
            "Kabuterimon": 2,
            "Seadramon": 2,
            "Garurumon": 2,
            "Sukamon": 1,
            "MetalGreymon": 3,
            "SkullGreymon": 3,
            "Giromon": 3,
            "Mamemon": 3,
            "Monzaemon": 3,
            "Digitamamon": 3,
            "Andromon": 3,
            "Megadramon": 3,
            "Piximon": 3,
            "MetalMamemon": 3,
            "Vademon": 3,
            "Etemon": 3        
            }
    return digimon_prosperity_points

def calculate_prosperity_points(state, self) -> int:
    total_prosperity_points = 0
    digimon_prosperity_points = get_digimon_prosperity_list(self)


    for digimon, points in digimon_prosperity_points.items():
        if state.has(digimon, self.player):
            total_prosperity_points += points

    return total_prosperity_points

def calculate_reachable_prosperity_points(state, self, digimon=None) -> int:
    total_prosperity_points = 0
    digimon_prosperity_points = get_digimon_prosperity_list(self)

    if digimon =="Ogremon":
        digimon_prosperity_points.pop("Ogremon")
        digimon_prosperity_points.pop("Devimon")
        digimon_prosperity_points.pop("Digitamamon")
        digimon_prosperity_points.pop("Megadramon")
        digimon_prosperity_points.pop("Greymon")
        digimon_prosperity_points.pop("MetalGreymon")
        digimon_prosperity_points.pop("Airdramon")
        digimon_prosperity_points.pop("Vademon")
        digimon_prosperity_points.pop("Etemon")
        digimon_prosperity_points.pop("Ninjamon")
        digimon_prosperity_points.pop("Leomon")
    elif digimon =="Greymon":
        digimon_prosperity_points.pop("Greymon")
        digimon_prosperity_points.pop("Devimon")
        digimon_prosperity_points.pop("Digitamamon")
        digimon_prosperity_points.pop("Megadramon")
        digimon_prosperity_points.pop("MetalGreymon")
        digimon_prosperity_points.pop("Airdramon")
        digimon_prosperity_points.pop("Vademon")
        digimon_prosperity_points.pop("Etemon")
        digimon_prosperity_points.pop("Ninjamon")
        digimon_prosperity_points.pop("Leomon")
    elif digimon =="Vademon":
        digimon_prosperity_points.pop("Vademon")
        digimon_prosperity_points.pop("Devimon")
        digimon_prosperity_points.pop("Digitamamon")
        digimon_prosperity_points.pop("Megadramon")
        digimon_prosperity_points.pop("MetalGreymon")
        digimon_prosperity_points.pop("Airdramon")
        digimon_prosperity_points.pop("Etemon")
        digimon_prosperity_points.pop("Ninjamon")
        digimon_prosperity_points.pop("Leomon")
    elif digimon == "Airdramon":
        digimon_prosperity_points.pop("Airdramon")
        digimon_prosperity_points.pop("Devimon")
        digimon_prosperity_points.pop("Etemon")
        digimon_prosperity_points.pop("Digitamamon")
        digimon_prosperity_points.pop("Megadramon")
        digimon_prosperity_points.pop("MetalGreymon")
        digimon_prosperity_points.pop("Ninjamon")
        digimon_prosperity_points.pop("Leomon")
    elif digimon == "Etemon":
        digimon_prosperity_points.pop("Airdramon")
        digimon_prosperity_points.pop("Etemon")
        digimon_prosperity_points.pop("Devimon")
        digimon_prosperity_points.pop("Digitamamon")
        digimon_prosperity_points.pop("Megadramon")
        digimon_prosperity_points.pop("MetalGreymon")
        digimon_prosperity_points.pop("Ninjamon")
        digimon_prosperity_points.pop("Leomon")
    elif digimon == "Ninjamon":
        digimon_prosperity_points.pop("Airdramon")
        digimon_prosperity_points.pop("MetalGreymon")
        digimon_prosperity_points.pop("Devimon")
        digimon_prosperity_points.pop("Digitamamon")
        digimon_prosperity_points.pop("Megadramon")
        digimon_prosperity_points.pop("Ninjamon")
        digimon_prosperity_points.pop("Etemon")
        digimon_prosperity_points.pop("Leomon")
    elif digimon == "Leomon":
        digimon_prosperity_points.pop("Airdramon")
        digimon_prosperity_points.pop("MetalGreymon")
        digimon_prosperity_points.pop("Devimon")
        digimon_prosperity_points.pop("Digitamamon")
        digimon_prosperity_points.pop("Megadramon")
        digimon_prosperity_points.pop("Etemon")
        digimon_prosperity_points.pop("Ninjamon")
        digimon_prosperity_points.pop("Leomon")
    elif digimon == "MetalGreymon":
        digimon_prosperity_points.pop("Airdramon")
        digimon_prosperity_points.pop("MetalGreymon")
        digimon_prosperity_points.pop("Devimon")
        digimon_prosperity_points.pop("Digitamamon")
        digimon_prosperity_points.pop("Megadramon")
        digimon_prosperity_points.pop("Etemon")
        digimon_prosperity_points.pop("Ninjamon")
        digimon_prosperity_points.pop("Leomon")
    elif digimon == "Devimon":
        digimon_prosperity_points.pop("Airdramon")
        digimon_prosperity_points.pop("MetalGreymon")
        digimon_prosperity_points.pop("Devimon")
        digimon_prosperity_points.pop("Digitamamon")
        digimon_prosperity_points.pop("Megadramon")
        digimon_prosperity_points.pop("Etemon")
        digimon_prosperity_points.pop("Ninjamon")
        digimon_prosperity_points.pop("Leomon")
    elif digimon == "Digitamamon":
        digimon_prosperity_points.pop("Airdramon")
        digimon_prosperity_points.pop("MetalGreymon")
        digimon_prosperity_points.pop("Devimon")
        digimon_prosperity_points.pop("Digitamamon")
        digimon_prosperity_points.pop("Megadramon")
        digimon_prosperity_points.pop("Etemon")
        digimon_prosperity_points.pop("Ninjamon")
        digimon_prosperity_points.pop("Leomon")
    elif digimon == "Megadramon":
        digimon_prosperity_points.pop("Airdramon")
        digimon_prosperity_points.pop("MetalGreymon")
        digimon_prosperity_points.pop("Devimon")
        digimon_prosperity_points.pop("Digitamamon")
        digimon_prosperity_points.pop("Megadramon")
        digimon_prosperity_points.pop("Etemon")
        digimon_prosperity_points.pop("Ninjamon")
        digimon_prosperity_points.pop("Leomon")

    for iterdigimon, points in digimon_prosperity_points.items():        
        location = self.multiworld.get_location(iterdigimon, self.player)
        if location.can_reach(state):
            total_prosperity_points += points


    return total_prosperity_points

def can_get_points(self, state, amount):
    if amount >= 3:
        return False
    else:
        availableDigimon = get_digimon_prosperity_list(self)
        for digimon, prosperity in list(availableDigimon.items()):
            if state.has(digimon, self.player):
                availableDigimon.pop(digimon)
                continue
            if state.can_reach(self.multiworld.get_location(digimon, self.player)):
                availableDigimon.pop(digimon)
                continue
        if any(value == amount for value in availableDigimon.values()):
            return True

            
        
