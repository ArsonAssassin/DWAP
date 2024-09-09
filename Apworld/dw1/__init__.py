# world/dc2/__init__.py
from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification
from Options import Toggle

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule

from .Items import DigimonWorldItem, DigimonWorldItemCategory, item_dictionary, key_item_names, key_item_categories, item_descriptions, BuildItemPool
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
        self.enabled_location_categories.add(DigimonWorldLocationCategory.RECRUIT)
        self.enabled_location_categories.add(DigimonWorldLocationCategory.MISC)
        self.enabled_location_categories.add(DigimonWorldLocationCategory.EVENT)


    def create_regions(self):
        # Create Regions
        regions: Dict[str, Region] = {}
        regions["Menu"] = self.create_region("Menu", [])
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
            "Recruitment", "Prosperity", "Misc"
        ]})
        

        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])
            print(f"Connecting {from_region} to {to_region} Using entrance: " + connection.name)
            
        #regions["Menu"].create_exit("Recruitment", regions["Recruitment"])
        recruitEntrance = Entrance(self.player, "Enter Recruitment", regions["Menu"])
        prospEntrance = Entrance(self.player, "Enter Prosperity", regions["Menu"])
        miscEntrance = Entrance(self.player, "Enter Misc", regions["Menu"])
        regions["Menu"].exits.append(recruitEntrance)
        regions["Menu"].exits.append(prospEntrance)
        regions["Menu"].exits.append(miscEntrance)
        recruitEntrance.connect(regions["Recruitment"])
        prospEntrance.connect(regions["Prosperity"])
        miscEntrance.connect(regions["Misc"])
        
    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)
        #print("location table size: " + str(len(location_table)))
        for location in location_table:
            #print("Creating location: " + location.name)
            if location.category in self.enabled_location_categories and location.category != DigimonWorldLocationCategory.RECRUIT:
                #print("Adding location: " + location.name + " with default item " + location.default_item)
                new_location = DigimonWorldLocation(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region
                )
            else:
                # Replace non-randomized progression items with events
                event_item = self.create_item(location.default_item)
                #if event_item.classification != ItemClassification.progression:
                #    continue
                #print("Adding Location: " + location.name + " as an event with default item " + location.default_item)
                new_location = DigimonWorldLocation(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    None,
                    new_region
                )
                event_item.code = None
                new_location.place_locked_item(event_item)
                #print("Placing event: " + event_item.name + " in location: " + location.name)

            new_region.locations.append(new_location)
        print("created " + str(len(new_region.locations)) + " locations")
        self.multiworld.regions.append(new_region)
        print("adding region: " + region_name)
        return new_region


    def create_items(self):
        skip_items: List[DigimonWorldItem] = []
        itempool: List[DigimonWorldItem] = []
        itempoolSize = 0
        
        early_unlock = None
        #print("Creating items")
        for location in self.multiworld.get_locations(self.player):
            if location.name == "Free Starter Soul":
                early_game_digimon = ["Betamon", "Palmon", "Coelamon", "Bakemon", "Centarumon", "Kunemon"]
                early_unlock = random.choice(early_game_digimon)
                starter_soul = self.create_item(early_unlock + " Soul")
                location.place_locked_item(starter_soul)
                continue
               
            #print("found item in category: " + str(location.category))
            item_data = item_dictionary[location.default_item_name]
            if item_data.category in [DigimonWorldItemCategory.SKIP, DigimonWorldItemCategory.EVENT, DigimonWorldItemCategory.RECRUIT] or location.category == DigimonWorldLocationCategory.RECRUIT:
                #print("Adding skip item: " + location.default_item_name)
                skip_items.append(self.create_item(location.default_item_name))
            elif location.category in self.enabled_location_categories:
                if(location.name == "1 Prosperity" and self.options.early_statcap.value):
                    continue
                #print("Adding item: " + location.default_item_name)
                itempoolSize += 1
                itempool.append(self.create_item(location.default_item_name))
        
        print("Requesting itempool size: " + str(itempoolSize))
        foo = BuildItemPool(itempoolSize, self.options, early_unlock)
        print("Created item pool size: " + str(len(foo)))
        if self.options.early_statcap.value:
            print("Adding early stat cap item")
            location = self.multiworld.get_location("1 Prosperity", self.player)
            location.place_locked_item(self.create_item("Progressive Stat Cap"))

        removable_items = [item for item in itempool if item.classification != ItemClassification.progression]
        print("marked " + str(len(removable_items)) + " items as removable")
        
        for item in removable_items:
            itempool.remove(item)
            itempool.append(self.create_item(foo.pop().name))

        # Add regular items to itempool
        self.multiworld.itempool += itempool

        # Handle SKIP items separately
        for skip_item in skip_items:
            location = next(loc for loc in self.multiworld.get_locations(self.player) 
                            if loc.default_item_name == skip_item.name)
            location.place_locked_item(skip_item)
            #self.multiworld.itempool.append(skip_item)
            #print("Placing skip item: " + skip_item.name + " in location: " + location.name)
        

    def create_item(self, name: str) -> Item:
        useful_categories = {
            DigimonWorldItemCategory.CONSUMABLE,
            DigimonWorldItemCategory.DV,
            DigimonWorldItemCategory.MISC,
        }
        data = self.item_name_to_id[name]

        if name in key_item_names or item_dictionary[name].category in key_item_categories:
            item_classification = ItemClassification.progression
        elif item_dictionary[name].category in useful_categories:
            item_classification = ItemClassification.useful
        else:
            item_classification = ItemClassification.filler

        return DigimonWorldItem(name, item_classification, data, self.player)

    def get_recruited_digimon(self, state) -> List[str]:
        recruited_digimon = []
        for digimon in recruit_digimon_list:            
            if state.has(digimon.name, self.player):
                recruited_digimon.append(digimon.name)
        return recruited_digimon

    def has_digimon_requirements(self, state, digimon) -> bool:
        existing_recruits = self.get_recruited_digimon(state)
        for requirement in digimon.digimon_requirements:
            if requirement not in existing_recruits:
                return False
        current_prosperity = sum([digimon.prosperity_value for digimon in recruit_digimon_list if digimon.name in existing_recruits])
        if not current_prosperity >= digimon.prosperity_requirement:
            return False
        has_soul = state.has(digimon.name + " Soul", self.player) or digimon.name == "Agumon"
        return has_soul
    
    def get_filler_item_name(self) -> str:
        return "1000 Bits"
        
    def set_rules(self) -> None:        
       
        print("Setting rules")

        required_prosperity_points = self.options.required_prosperity.value
        print("Setting completion condition for " + str(required_prosperity_points) + " prosperity points")
        completionLocation = self.multiworld.get_location(str(required_prosperity_points) + " Prosperity", self.player)
        self.multiworld.completion_condition[self.player] = lambda state: \
            completionLocation.can_reach(state)
        

        
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
