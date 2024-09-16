# world/dc2/__init__.py
from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification
from Options import Toggle

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule

from .Items import DigimonWorldItem, DigimonWorldItemCategory, item_dictionary, key_item_names, key_item_categories, item_descriptions, _all_items, BuildItemPool
from .Locations import DigimonWorldLocation, DigimonWorldLocationCategory, location_tables, location_dictionary
from .Options import DigimonWorldOption
from .RecruitDigimon import recruit_digimon_list
import random

class DigimonWorldWeb(WebWorld):
    bug_report_page = ""
    theme = "stone"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Digimon World randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["ArsonAssassin"]
    )


    tutorials = [setup_en]


class DigimonWorldWorld(World):
    """
    Digimon World is a game about raising digital monsters and recruiting allies to save the digital world.
    """

    game: str = "Digimon World"
    options_dataclass = DigimonWorldOption
    options: DigimonWorldOption
    topology_present: bool = True
    web = DigimonWorldWeb()
    data_version = 0
    base_id = 690000
    enabled_location_categories: Set[DigimonWorldLocationCategory]
    required_client_version = (0, 5, 0)
    item_name_to_id = DigimonWorldItem.get_name_to_id()
    location_name_to_id = DigimonWorldLocation.get_name_to_id()
    item_name_groups = {
    }
    item_descriptions = item_descriptions


    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []
        self.enabled_location_categories = set()


    def generate_early(self):
        self.enabled_location_categories.add(DigimonWorldLocationCategory.MISC)
        self.enabled_location_categories.add(DigimonWorldLocationCategory.EVENT)
        self.enabled_location_categories.add(DigimonWorldLocationCategory.RECRUIT)
        self.enabled_location_categories.add(DigimonWorldLocationCategory.CARD)
        


    def create_regions(self):
        # Create Regions
        regions: Dict[str, Region] = {}      
        regions["Menu"] = self.create_region("Menu", [])  
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
            "Start Game","Consumable", "Cards", "Prosperity",
            "Agumon", "Betamon","Greymon","Devimon","Airdramon","Tyrannomon","Meramon","Seadramon","Numemon","MetalGreymon","Mamemon","Monzaemon",
            "Gabumon","Elecmon","Kabuterimon","Angemon","Birdramon","Garurumon","Frigimon","Whamon","Vegiemon","SkullGreymon","MetalMamemon","Vademon",
            "Patamon","Kunemon","Unimon","Ogremon","Shellmon","Centarumon","Bakemon","Drimogemon","Sukamon","Andromon", "Giromon", "Etemon", "Biyomon",
            "Palmon", "Monochromon", "Leomon", "Coelamon", "Kokatorimon", "Kuwagamon", "Mojyamon", "Nanimon", "Megadramon", "Piximon", "Digitamamon",
            "Penguinmon", "Ninjamon"
        ]})
        

        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{from_region} -> {to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])
            #print(f"Connecting {from_region} to {to_region} Using entrance: " + connection.name)
        create_connection("Menu", "Start Game") 
        create_connection("Start Game", "Cards") 
        create_connection("Start Game", "Agumon") 
        create_connection("Start Game", "Prosperity") 

        create_connection("Agumon", "Betamon") 
        create_connection("Agumon", "Greymon")
        create_connection("Agumon", "Devimon")
        create_connection("Agumon", "Airdramon")
        create_connection("Agumon", "Tyrannomon")
        create_connection("Agumon", "Meramon")
        create_connection("Agumon", "Seadramon")
        create_connection("Agumon", "Numemon")
        create_connection("Agumon", "MetalGreymon")
        create_connection("Agumon", "Mamemon")
        create_connection("Agumon", "Monzaemon")
        create_connection("Agumon", "Gabumon")
        create_connection("Agumon", "Elecmon")
        create_connection("Agumon", "Kabuterimon")
        create_connection("Agumon", "Angemon")
        create_connection("Agumon", "Birdramon")
        create_connection("Agumon", "Garurumon")
        create_connection("Agumon", "Frigimon")
        create_connection("Agumon", "Whamon")
        create_connection("Agumon", "Vegiemon")
        create_connection("Agumon", "SkullGreymon")
        create_connection("Agumon", "MetalMamemon")
        create_connection("Agumon", "Vademon")
        create_connection("Agumon", "Patamon")
        create_connection("Agumon", "Kunemon")
        create_connection("Agumon", "Unimon")
        create_connection("Agumon", "Ogremon")
        create_connection("Agumon", "Shellmon")
        create_connection("Agumon", "Centarumon")
        create_connection("Agumon", "Bakemon")
        create_connection("Agumon", "Drimogemon")
        create_connection("Agumon", "Sukamon")
        create_connection("Agumon", "Andromon")
        create_connection("Agumon", "Giromon")
        create_connection("Agumon", "Etemon")
        create_connection("Agumon", "Biyomon")
        create_connection("Agumon", "Palmon")
        create_connection("Agumon", "Monochromon")
        create_connection("Agumon", "Leomon")
        create_connection("Agumon", "Coelamon")
        create_connection("Agumon", "Kokatorimon")
        create_connection("Agumon", "Kuwagamon")
        create_connection("Agumon", "Mojyamon")
        create_connection("Agumon", "Nanimon")
        create_connection("Agumon", "Megadramon")
        create_connection("Agumon", "Piximon")
        create_connection("Agumon", "Digitamamon")
        create_connection("Agumon", "Penguinmon")
        create_connection("Agumon", "Ninjamon")
        
    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)
        for location in location_table:
            if location.category in self.enabled_location_categories:
                new_location = DigimonWorldLocation(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region) 
            else:
                # Replace non-randomized progression items with events
                event_item = self.create_item(location.default_item)
                new_location = DigimonWorldLocation(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    None,
                    new_region)
                #event_item.code = None
                new_location.place_locked_item(event_item)
                print("Placing event: " + event_item.name + " in location: " + location.name)

            new_region.locations.append(new_location)
        self.multiworld.regions.append(new_region)
        return new_region


    def create_items(self):
        itempool: List[DigimonWorldItem] = []
        itempoolSize = 0
        for location in self.multiworld.get_locations(self.player):
            if location.category in self.enabled_location_categories:
                itempoolSize += 1

        print(f"Itempool size: {itempoolSize}")

        for item in _all_items:
            if item.category == DigimonWorldItemCategory.SOUL:
                if item.name == "Agumon Soul":
                    continue
                itempool.append(self.create_item(item.name))
                itempoolSize -= 1
            
        
        print(f"Itempool size after adding souls: {itempoolSize}")
        filler_pool = BuildItemPool(itempoolSize, self.options)
        for item in filler_pool:
            itempool.append(self.create_item(self.get_filler_item_name()))
            itempool.append(self.create_item(item.name))
            itempoolSize -= 1
        # for i in range(itempoolSize):
        #     itempool.append(self.create_item(self.get_filler_item_name()))
        #     itempoolSize -= 1
        print(f"Itempool size after adding fillers: {itempoolSize}")

        if self.options.early_statcap.value:
            # print("Adding early stat cap item")
            location = self.multiworld.get_location("1 Prosperity", self.player)
            location.place_locked_item(self.create_item("Progressive Stat Cap"))
        location = self.multiworld.get_location("Start Game", self.player)
        location.place_locked_item(self.create_item("Agumon Soul"))
        # Add regular items to itempool
        self.multiworld.itempool += itempool

        

    def create_item(self, name: str) -> Item:
        useful_categories = {
           # DigimonWorldItemCategory.CONSUMABLE,
           # DigimonWorldItemCategory.DV,
           # DigimonWorldItemCategory.MISC,
        }
        data = self.item_name_to_id[name]

        if name in key_item_names or item_dictionary[name].category in key_item_categories:
            item_classification = ItemClassification.progression
        elif item_dictionary[name].category in useful_categories:
            item_classification = ItemClassification.useful
        else:
            item_classification = ItemClassification.filler

        return DigimonWorldItem(name, item_classification, data, self.player)

    
    def get_filler_item_name(self) -> str:
        return "1000 Bits"
    
    def set_rules(self) -> None:  
        def get_recruited_digimon(self, state) -> List[str]:
            recruited_digimon = []
            for digimon in recruit_digimon_list: 
                if state.has(f"{digimon.name} Recruited", self.player):
                    recruited_digimon.append(digimon.name)                
            return recruited_digimon
        def calculate_prosperity(self, state):
            existing_recruits = get_recruited_digimon(self, state)
            current_prosperity = sum([digimon.prosperity_value for digimon in recruit_digimon_list if digimon.name in existing_recruits])
            return current_prosperity
        def has_digimon_requirements(self, state, digimon) -> bool:
            existing_recruits = self.get_recruited_digimon( state)
            for requirement in digimon.digimon_requirements:
                if requirement not in existing_recruits:
                    return False
                current_prosperity = self.calculate_prosperity(state)
                if not current_prosperity >= digimon.prosperity_requirement:
                    return False
                if not digimon.requires_soul:
                    return True            
                has_soul = state.has(digimon.name + " Soul", self.player)
                return has_soul
  
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Digitamamon Recruited", self.player)

        #for region in self.multiworld.get_regions(self.player):
        #    for location in region.locations:
        #            set_rule(location, lambda state: True)

        set_rule(self.multiworld.get_location("Start Game", self.player), lambda state: True)
        set_rule(self.multiworld.get_entrance(f"Menu -> Start Game", self.player),lambda state: True)
        set_rule(self.multiworld.get_entrance(f"Start Game -> Agumon", self.player), lambda state: state.has("Agumon Soul", self.player))


        set_rule(self.multiworld.get_entrance(f"Agumon -> Betamon", self.player), lambda state: state.has("Betamon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Betamon", self.player), lambda state: state.has("Betamon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Betamon Recruited", self.player), lambda state: state.has("Betamon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Kunemon", self.player), lambda state: state.has("Kunemon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Kunemon", self.player), lambda state: state.has("Kunemon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Kunemon Recruited", self.player), lambda state: state.has("Kunemon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Palmon", self.player), lambda state: state.has("Palmon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Palmon", self.player), lambda state: state.has("Palmon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Palmon Recruited", self.player), lambda state: state.has("Palmon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Bakemon", self.player), lambda state: state.has("Bakemon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Bakemon", self.player), lambda state: state.has("Bakemon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Bakemon Recruited", self.player), lambda state: state.has("Bakemon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Centarumon", self.player), lambda state: state.has("Centarumon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Centarumon", self.player), lambda state: state.has("Centarumon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Centarumon Recruited", self.player), lambda state: state.has("Centarumon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Coelamon", self.player), lambda state: state.has("Coelamon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Coelamon", self.player), lambda state: state.has("Coelamon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Coelamon Recruited", self.player), lambda state: state.has("Coelamon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Gabumon", self.player), lambda state: state.has("Gabumon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Gabumon", self.player), lambda state: state.has("Gabumon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Gabumon Recruited", self.player), lambda state: state.has("Gabumon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Greymon", self.player), lambda state: state.has("Greymon Soul", self.player) and calculate_prosperity(self, state) >= 15 and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Greymon", self.player), lambda state: state.has("Greymon Soul", self.player) and calculate_prosperity(self, state) >= 15 and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Greymon Recruited", self.player), lambda state: state.has("Greymon Soul", self.player) and calculate_prosperity(self, state) >= 15 and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Monochromon", self.player), lambda state: state.has("Monochromon Soul", self.player) and calculate_prosperity(self, state) >= 6 and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Monochromon", self.player), lambda state: state.has("Monochromon Soul", self.player) and calculate_prosperity(self, state) >= 6 and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Monochromon Recruited", self.player), lambda state: state.has("Monochromon Soul", self.player) and calculate_prosperity(self, state) >= 6 and state.has("Agumon Recruited", self.player))   

        set_rule(self.multiworld.get_entrance(f"Agumon -> Meramon", self.player), lambda state: state.has("Meramon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Meramon", self.player), lambda state: state.has("Meramon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Meramon Recruited", self.player), lambda state: state.has("Meramon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Elecmon", self.player), lambda state: state.has("Elecmon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Elecmon", self.player), lambda state: state.has("Elecmon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Elecmon Recruited", self.player), lambda state: state.has("Elecmon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Patamon", self.player), lambda state: state.has("Patamon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Patamon", self.player), lambda state: state.has("Patamon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Patamon Recruited", self.player), lambda state: state.has("Patamon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Biyomon", self.player), lambda state: state.has("Biyomon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Biyomon", self.player), lambda state: state.has("Biyomon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Biyomon Recruited", self.player), lambda state: state.has("Biyomon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Sukamon", self.player), lambda state: state.has("Sukamon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Sukamon", self.player), lambda state: state.has("Sukamon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Sukamon Recruited", self.player), lambda state: state.has("Sukamon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Tyrannomon", self.player), lambda state: state.has("Tyrannomon Soul", self.player) and state.has("Centarumon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Tyrannomon", self.player), lambda state: state.has("Tyrannomon Soul", self.player) and state.has("Centarumon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Tyrannomon Recruited", self.player), lambda state: state.has("Tyrannomon Soul", self.player) and state.has("Centarumon Recruited", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Birdramon", self.player), lambda state: state.has("Birdramon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Birdramon", self.player), lambda state: state.has("Birdramon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Birdramon Recruited", self.player), lambda state: state.has("Birdramon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Unimon", self.player), lambda state: state.has("Unimon Soul", self.player) and state.has("Centarumon Recruited", self.player) and state.has("Meramon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Unimon", self.player), lambda state: state.has("Unimon Soul", self.player) and state.has("Centarumon Recruited", self.player) and state.has("Meramon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Unimon Recruited", self.player), lambda state: state.has("Unimon Soul", self.player) and state.has("Centarumon Recruited", self.player) and state.has("Meramon Recruited", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Penguinmon", self.player), lambda state: state.has("Penguinmon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Penguinmon", self.player), lambda state: state.has("Penguinmon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Penguinmon Recruited", self.player), lambda state: state.has("Penguinmon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Mojyamon", self.player), lambda state: state.has("Mojyamon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Mojyamon", self.player), lambda state: state.has("Mojyamon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Mojyamon Recruited", self.player), lambda state: state.has("Mojyamon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Angemon", self.player), lambda state: state.has("Angemon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Angemon", self.player), lambda state: state.has("Angemon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Angemon Recruited", self.player), lambda state: state.has("Angemon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Vegiemon", self.player), lambda state: state.has("Vegiemon Soul", self.player) and state.has("Palmon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Vegiemon", self.player), lambda state: state.has("Vegiemon Soul", self.player) and state.has("Palmon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Vegiemon Recruited", self.player), lambda state: state.has("Vegiemon Soul", self.player) and state.has("Palmon Recruited", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Shellmon", self.player), lambda state: state.has("Shellmon Soul", self.player) and calculate_prosperity(self, state) >= 6) and state.has("Agumon Recruited", self.player)
        set_rule(self.multiworld.get_location(f"Shellmon", self.player), lambda state: state.has("Shellmon Soul", self.player) and calculate_prosperity(self, state) >= 6 and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Shellmon Recruited", self.player), lambda state: state.has("Shellmon Soul", self.player) and calculate_prosperity(self, state) >= 6 and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Piximon", self.player), lambda state: state.has("Piximon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Piximon", self.player), lambda state: state.has("Piximon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Piximon Recruited", self.player), lambda state: state.has("Piximon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Whamon", self.player), lambda state: state.has("Whamon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Whamon", self.player), lambda state: state.has("Whamon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Whamon Recruited", self.player), lambda state: state.has("Whamon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Numemon", self.player), lambda state: state.has("Numemon Soul", self.player) and state.has("Whamon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Numemon", self.player), lambda state: state.has("Numemon Soul", self.player) and state.has("Whamon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Numemon Recruited", self.player), lambda state: state.has("Numemon Soul", self.player) and state.has("Whamon Recruited", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Giromon", self.player), lambda state: state.has("Giromon Soul", self.player) and state.has("Whamon Recruited", self.player) and state.has("Numemon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Giromon", self.player), lambda state: state.has("Giromon Soul", self.player) and state.has("Whamon Recruited", self.player) and state.has("Numemon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Giromon Recruited", self.player), lambda state: state.has("Giromon Soul", self.player) and state.has("Whamon Recruited", self.player) and state.has("Numemon Recruited", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Andromon", self.player), lambda state: state.has("Andromon Soul", self.player) and state.has("Whamon Recruited", self.player) and state.has("Numemon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Andromon", self.player), lambda state: state.has("Andromon Soul", self.player) and state.has("Whamon Recruited", self.player) and state.has("Numemon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Andromon Recruited", self.player), lambda state: state.has("Andromon Soul", self.player) and state.has("Whamon Recruited", self.player) and state.has("Numemon Recruited", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Frigimon", self.player), lambda state: state.has("Frigimon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Frigimon", self.player), lambda state: state.has("Frigimon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Frigimon Recruited", self.player), lambda state: state.has("Frigimon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Seadramon", self.player), lambda state: state.has("Seadramon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Seadramon", self.player), lambda state: state.has("Seadramon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Seadramon Recruited", self.player), lambda state: state.has("Seadramon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Garurumon", self.player), lambda state: state.has("Garurumon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Garurumon", self.player), lambda state: state.has("Garurumon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Garurumon Recruited", self.player), lambda state: state.has("Garurumon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Monzaemon", self.player), lambda state: state.has("Monzaemon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Monzaemon", self.player), lambda state: state.has("Monzaemon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Monzaemon Recruited", self.player), lambda state: state.has("Monzaemon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Kokatorimon", self.player), lambda state: state.has("Kokatorimon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Kokatorimon", self.player), lambda state: state.has("Kokatorimon Soul", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Kokatorimon Recruited", self.player), lambda state: state.has("Kokatorimon Soul", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Ogremon", self.player), lambda state: state.has("Ogremon Soul", self.player) and calculate_prosperity(self, state) >= 6 and state.has("Whamon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Ogremon", self.player), lambda state: state.has("Ogremon Soul", self.player) and calculate_prosperity(self, state) >= 6 and state.has("Whamon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Ogremon Recruited", self.player), lambda state: state.has("Ogremon Soul", self.player) and calculate_prosperity(self, state) >= 6 and state.has("Whamon Recruited", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Kuwagamon", self.player), lambda state: state.has("Kuwagamon Soul", self.player) and state.has("Seadramon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Kuwagamon", self.player), lambda state: state.has("Kuwagamon Soul", self.player) and state.has("Seadramon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Kuwagamon Recruited", self.player), lambda state: state.has("Kuwagamon Soul", self.player) and state.has("Seadramon Recruited", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Kabuterimon", self.player), lambda state: state.has("Kabuterimon Soul", self.player) and state.has("Seadramon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Kabuterimon", self.player), lambda state: state.has("Kabuterimon Soul", self.player) and state.has("Seadramon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Kabuterimon Recruited", self.player), lambda state: state.has("Kabuterimon Soul", self.player) and state.has("Seadramon Recruited", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Drimogemon", self.player), lambda state: state.has("Drimogemon Soul", self.player) and state.has("Meramon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Drimogemon", self.player), lambda state: state.has("Drimogemon Soul", self.player) and state.has("Meramon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Drimogemon Recruited", self.player), lambda state: state.has("Drimogemon Soul", self.player) and state.has("Meramon Recruited", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Vademon", self.player), lambda state: state.has("Vademon Soul", self.player) and calculate_prosperity(self, state) >= 45 and state.has("Meramon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Vademon", self.player), lambda state: state.has("Vademon Soul", self.player) and calculate_prosperity(self, state) >= 45 and state.has("Meramon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Vademon Recruited", self.player), lambda state: state.has("Vademon Soul", self.player) and calculate_prosperity(self, state) >= 45 and state.has("Meramon Recruited", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> MetalMamemon", self.player), lambda state: state.has("MetalMamemon Soul", self.player) and state.has("Whamon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"MetalMamemon", self.player), lambda state: state.has("MetalMamemon Soul", self.player) and state.has("Whamon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"MetalMamemon Recruited", self.player), lambda state: state.has("MetalMamemon Soul", self.player) and state.has("Whamon Recruited", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> SkullGreymon", self.player), lambda state: state.has("SkullGreymon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Greymon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"SkullGreymon", self.player), lambda state: state.has("SkullGreymon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Greymon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"SkullGreymon Recruited", self.player), lambda state: state.has("SkullGreymon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Greymon Recruited", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Mamemon", self.player), lambda state: state.has("Mamemon Soul", self.player) and state.has("Meramon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Mamemon", self.player), lambda state: state.has("Mamemon Soul", self.player) and state.has("Meramon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Mamemon Recruited", self.player), lambda state: state.has("Mamemon Soul", self.player) and state.has("Meramon Recruited", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Ninjamon", self.player), lambda state: state.has("Ninjamon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Ninjamon", self.player), lambda state: state.has("Ninjamon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Ninjamon Recruited", self.player), lambda state: state.has("Ninjamon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Devimon", self.player), lambda state: state.has("Devimon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))    
        set_rule(self.multiworld.get_location(f"Devimon", self.player), lambda state: state.has("Devimon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Devimon Recruited", self.player), lambda state: state.has("Devimon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Leomon", self.player), lambda state: state.has("Leomon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Meramon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Leomon", self.player), lambda state: state.has("Leomon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Meramon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Leomon Recruited", self.player), lambda state: state.has("Leomon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Meramon Recruited", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Nanimon", self.player), lambda state: state.has("Nanimon Soul", self.player) and state.has("Numemon Recruited", self.player) and state.has("Leomon Recruited", self.player) and state.has("Tyrannomon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Nanimon", self.player), lambda state: state.has("Nanimon Soul", self.player) and state.has("Numemon Recruited", self.player) and state.has("Leomon Recruited", self.player) and state.has("Tyrannomon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Nanimon Recruited", self.player), lambda state: state.has("Nanimon Soul", self.player) and state.has("Numemon Recruited", self.player) and state.has("Leomon Recruited", self.player) and state.has("Tyrannomon Recruited", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> MetalGreymon", self.player), lambda state: state.has("MetalGreymon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Greymon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"MetalGreymon", self.player), lambda state: state.has("MetalGreymon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Greymon Recruited", self.player) and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"MetalGreymon Recruited", self.player), lambda state: state.has("MetalGreymon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Greymon Recruited", self.player) and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Etemon", self.player), lambda state: state.has("Etemon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Etemon", self.player), lambda state: state.has("Etemon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Etemon Recruited", self.player), lambda state: state.has("Etemon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Megadramon", self.player), lambda state: state.has("Megadramon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Megadramon", self.player), lambda state: state.has("Megadramon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Megadramon Recruited", self.player), lambda state: state.has("Megadramon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Airdramon", self.player), lambda state: state.has("Airdramon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Airdramon", self.player), lambda state: state.has("Airdramon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Airdramon Recruited", self.player), lambda state: state.has("Airdramon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))

        set_rule(self.multiworld.get_entrance(f"Agumon -> Digitamamon", self.player), lambda state: state.has("Digitamamon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Digitamamon", self.player), lambda state: state.has("Digitamamon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))
        set_rule(self.multiworld.get_location(f"Digitamamon Recruited", self.player), lambda state: state.has("Digitamamon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))

        for card in [card for card in self.multiworld.get_locations(self.player) if card.category == DigimonWorldLocationCategory.CARD]:            
            if(card.name == "Machinedramon Card"):
                set_rule(card, lambda state: state.has("Digitamamon Soul", self.player) and calculate_prosperity(self, state) >= 50 and state.has("Agumon Recruited", self.player))
                continue
            set_rule(card, lambda state: state.has("Meramon Recruited", self.player))

        set_rule(self.multiworld.get_location(f"1 Prosperity", self.player), lambda state: state.has("Agumon Recruited", self.player))
        for prosperity_location in self.multiworld.get_locations(self.player):   
            if prosperity_location.name.endswith("Prosperity"):                
                prosperity_value = int(prosperity_location.name.split(" ")[0])
                current_prosperity = lambda state, player: sum(digimon.prosperity_value for digimon in recruit_digimon_list if self.multiworld.get_location(digimon.name, player).can_reach(state))                
                set_rule(prosperity_location, lambda state: current_prosperity(state, self.player) >= prosperity_value and state.has("Agumon Recruited", self.player))
        #completionLocation = self.multiworld.get_location("Digitamamon", self.player)    

            #completionLocation.can_reach(state)
        #    calculate_prosperity(self, state) >= 1#self.options.required_prosperity.value 
    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}


        name_to_dw_code = {item.name: item.dw_code for item in item_dictionary.values()}
        # Create the mandatory lists to generate the player's output file
        items_id = []
        items_address = []
        locations_id = []
        locations_address = []
        locations_target = []
        for location in self.multiworld.get_filled_locations():


            if location.item.player == self.player:
                #we are the receiver of the item
                items_id.append(location.item.code)
                items_address.append(name_to_dw_code[location.item.name])


            if location.player == self.player:
                #we are the sender of the location check
                locations_address.append(item_dictionary[location_dictionary[location.name].default_item].dw_code)
                locations_id.append(location.address)
                if location.item.player == self.player:
                    locations_target.append(name_to_dw_code[location.item.name])
                else:
                    locations_target.append(0)

        slot_data = {
            "options": {
                #"goal": self.options.goal.value,
                "required_prosperity": self.options.required_prosperity.value,
                "guaranteed_items": self.options.guaranteed_items.value,
                "exp_multiplier": self.options.exp_multiplier.value,
                "progressive_stats": self.options.progressive_stats.value,
                "random_starter": self.options.random_starter.value,
                "early_statcap": self.options.early_statcap.value,
                "random_techniques": self.options.random_techniques.value
            },
            "seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "slot": self.multiworld.player_name[self.player],  # to connect to server
            "base_id": self.base_id,  # to merge location and items lists
            "locationsId": locations_id,
            "locationsAddress": locations_address,
            "locationsTarget": locations_target,
            "itemsId": items_id,
            "itemsAddress": items_address
        }

        return slot_data
