# world/dc2/__init__.py
from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification
from Options import Toggle

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule

from .Items import DigimonWorldItem, DigimonWorldItemCategory, item_dictionary, key_item_names, item_descriptions
from .Locations import DigimonWorldLocation, DigimonWorldLocationCategory, location_tables, location_dictionary
from .Options import digimon_world_options
from .Prosperity import calculate_prosperity_points

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
    Digimon World is a game.
    """

    game: str = "Digimon World"
    option_definitions = digimon_world_options
    topology_present: bool = True
    web = DigimonWorldWeb()
    data_version = 0
    base_id = 690000
    enabled_location_categories: Set[DigimonWorldLocationCategory]
    required_client_version = (0, 4, 6)
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
            "Recruitment", "Prosperity"
        ]})
        

        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])

        regions["Menu"].exits.append(Entrance(self.player, "New Game", regions["Menu"]))
        self.multiworld.get_entrance("New Game", self.player).connect(regions["Recruitment"])
        self.multiworld.get_entrance("New Game", self.player).connect(regions["Prosperity"])
       # create_connection("Palm Brinks", "Underground Water Channel")

        
        
    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)

        for location in location_table:
            if location.category in self.enabled_location_categories:
                print("Adding location: " + location.name + " with default item " + location.default_item)
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
                if event_item.classification != ItemClassification.progression:
                    continue
                print("Adding Location: " + location.name + " as an event with default item " + location.default_item)
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
                print("Placing event: " + event_item.name + " in location: " + location.name)

            if region_name == "Menu":
                add_item_rule(new_location, lambda item: not item.advancement)

            new_region.locations.append(new_location)
            print("created " + str(len(new_region.locations)) + " locations")
        self.multiworld.regions.append(new_region)
        return new_region


    def create_items(self):
        itempool_by_category = {category: [] for category in self.enabled_location_categories}
        skip_items = []
        print("Creating items")
        for location in self.multiworld.get_locations(self.player):
            if location.category in itempool_by_category:
                item_data = item_dictionary[location.default_item_name]
                if item_data.category == DigimonWorldItemCategory.SKIP or item_data.category == DigimonWorldItemCategory.EVENT or item_data.category == DigimonWorldItemCategory.RECRUIT:
                    print("Adding skip item: " + location.default_item_name)
                    skip_items.append(self.create_item(location.default_item_name))
                else:
                    print("Adding item: " + location.default_item_name)
                    itempool_by_category[location.category].append(location.default_item_name)

        itempool: List[DigimonWorldItem] = []
        for category in itempool_by_category:
            itempool += [self.create_item(name) for name in itempool_by_category[category]]
        if(self.multiworld.progressive_stats[self.player].value):
            for _ in range(9):
                itempool += [self.create_item("Progressive Stat Cap")]
        print("created item pool with " + str(len(itempool)) + " items")
        removable_items = [item for item in itempool if item.classification != ItemClassification.progression]
        print("marked " + str(len(removable_items)) + " items as removable")
        guaranteed_items = self.multiworld.guaranteed_items[self.player].value
        for item_name in guaranteed_items:
            if len(removable_items) == 0:
                break
            num_existing_copies = len([item for item in itempool if item.name == item_name])
            for _ in range(guaranteed_items[item_name]):
                if num_existing_copies > 0:
                    num_existing_copies -= 1
                    continue
                if len(removable_items) == 0:
                    break
                removable_shortlist = [
                    item for item
                    in removable_items
                    if item_dictionary[item.name].category == item_dictionary[item_name].category
                ]
                if len(removable_shortlist) == 0:
                    removable_shortlist = removable_items
                removed_item = self.multiworld.random.choice(removable_shortlist)
                print(f"Replacing {removed_item.name} with {item_name}")
                removable_items.remove(removed_item)
                itempool.remove(removed_item)
                itempool.append(self.create_item(item_name))

        # Add regular items to itempool
        self.multiworld.itempool += itempool

        # Handle SKIP items separately
        for skip_item in skip_items:
            location = next(loc for loc in self.multiworld.get_locations(self.player) 
                            if loc.default_item_name == skip_item.name)
            location.place_locked_item(skip_item)
            self.multiworld.itempool.append(skip_item)
            print("Placing skip item: " + skip_item.name + " in location: " + location.name)


    def create_item(self, name: str) -> Item:
        useful_categories = {
            DigimonWorldItemCategory.CONSUMABLE,
            DigimonWorldItemCategory.MISC,
        }
        data = self.item_name_to_id[name]

        if name in key_item_names:
            item_classification = ItemClassification.progression
        elif item_dictionary[name].category in useful_categories:
            item_classification = ItemClassification.useful
        else:
            item_classification = ItemClassification.filler

        return DigimonWorldItem(name, item_classification, data, self.player)


    def get_filler_item_name(self) -> str:
        return "1000 Bits"


    #def set_rules(self) -> None:
        # Define the access rules to the entrances
        # set_rule(self.multiworld.get_location("Airdramon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Palmon", self.player),
                  # lambda state: state.has("Agumon", self.player))       
        # set_rule(self.multiworld.get_location("Kunemon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Meramon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Betamon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Coelamon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Piximon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Centarumon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Monochromon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Bakemon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Elecmon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Patamon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Biyomon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Greymon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Angemon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Birdramon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Frigimon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Gabumon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Garurumon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Kokatorimon", self.player),
                  # lambda state: state.has("Agumon", self.player))  
        # set_rule(self.multiworld.get_location("Mamemon", self.player),
                  # lambda state: state.has("Agumon", self.player))     
        # set_rule(self.multiworld.get_location("Mojyamon", self.player),
                  # lambda state: state.has("Agumon", self.player))     
        # set_rule(self.multiworld.get_location("Monzaemon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Penguinmon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Seadramon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Shellmon", self.player),
                  # lambda state: state.has("Agumon", self.player))    
        # set_rule(self.multiworld.get_location("Sukamon", self.player),
                  # lambda state: state.has("Agumon", self.player))   
        # set_rule(self.multiworld.get_location("Whamon", self.player),
                  # lambda state: state.has("Agumon", self.player))   
        
          
        # set_rule(self.multiworld.get_location("Kuwagamon", self.player),
                  # lambda state: state.has("Seadramon", self.player))    
        # set_rule(self.multiworld.get_location("Kabuterimon", self.player),
                  # lambda state: state.has("Seadramon", self.player))   
         
        # set_rule(self.multiworld.get_location("MetalMamemon", self.player),
                  # lambda state: state.has("Whamon", self.player))    
        # set_rule(self.multiworld.get_location("SkullGreymon", self.player),
                  # lambda state: state.has("Greymon", self.player))    
        # set_rule(self.multiworld.get_location("Airdramon", self.player),
                  # lambda state: state.has("MetalGreymon", self.player))                       
        # set_rule(self.multiworld.get_location("Digitamamon", self.player),
                  # lambda state: state.has("Airdramon", self.player))  
        # set_rule(self.multiworld.get_location("Drimogemon", self.player),
                  # lambda state: state.has("Meramon", self.player)) 
                      
        # set_rule(self.multiworld.get_location("Unimon", self.player),
                  # lambda state: state.has("Centarumon", self.player))    
        # set_rule(self.multiworld.get_location("Tyrannomon", self.player),
                  # lambda state: state.has("Centarumon", self.player))    
        # set_rule(self.multiworld.get_location("Nanimon", self.player),
                  # lambda state: state.has("Tyrannomon", self.player))    
        # set_rule(self.multiworld.get_location("Nanimon", self.player),
                  # lambda state: state.has("Leomon", self.player))    
        # set_rule(self.multiworld.get_location("Nanimon", self.player),
                  # lambda state: state.has("Andromon", self.player))    
        # set_rule(self.multiworld.get_location("Andromon", self.player),
                  # lambda state: state.has("Numemon", self.player))    
        # set_rule(self.multiworld.get_location("Numemon", self.player),
                  # lambda state: state.has("Giromon", self.player))    
        # set_rule(self.multiworld.get_location("Giromon", self.player),
                  # lambda state: state.has("Whamon", self.player))  
        # set_rule(self.multiworld.get_location("Vademon", self.player),
                  # lambda state: state.has("Shellmon", self.player))  
        # set_rule(self.multiworld.get_location("Vegiemon", self.player),
                  # lambda state: state.has("Palmon", self.player))         
 
        # set_rule(self.multiworld.get_location("Airdramon", self.player),
                  # lambda state: state.has("MetalGreymon", self.player))       
 
        # set_rule(self.multiworld.get_location("Devimon", self.player),
                  # lambda state: calculate_prosperity_points(state, self.player) >= 50) 
        # set_rule(self.multiworld.get_location("Megadramon", self.player),
                  # lambda state: calculate_prosperity_points(state, self.player) >= 50) 
        # set_rule(self.multiworld.get_location("Digitamamon", self.player),
                  # lambda state: calculate_prosperity_points(state, self.player) >= 50) 
        # set_rule(self.multiworld.get_location("MetalGreymon", self.player),
                  # lambda state: calculate_prosperity_points(state, self.player) >= 50) 

        # set_rule(self.multiworld.get_location("Ogremon", self.player),
                  # lambda state: calculate_prosperity_points(state, self.player) >= 6)  
        # set_rule(self.multiworld.get_location("Airdramon", self.player),
                  # lambda state: calculate_prosperity_points(state, self.player) >= 50)   
        # set_rule(self.multiworld.get_location("Greymon", self.player),
                  # lambda state: calculate_prosperity_points(state, self.player) >= 25)  
        # set_rule(self.multiworld.get_location("Vademon", self.player),
                  # lambda state: calculate_prosperity_points(state, self.player) >= 45) 
        # set_rule(self.multiworld.get_location("Etemon", self.player),
                  # lambda state: calculate_prosperity_points(state, self.player) >= 50) 
        # set_rule(self.multiworld.get_location("Ninjamon", self.player),
                  # lambda state: calculate_prosperity_points(state, self.player) >= 50) 
        # set_rule(self.multiworld.get_location("Leomon", self.player),
                  # lambda state: calculate_prosperity_points(state, self.player) >= 50) 
       
        # self.multiworld.completion_condition[self.player] = lambda state: \
        #             state.has("100 Prosperity", self.player)
        # self.multiworld.completion_condition[self.player] = lambda state: \
                    # calculate_prosperity_points(state, self.player) >= 100 
    
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
            print("Filling location: " + location.name)
            # Skip events
            if location.item.code is None:
                print("Skipping event: " + location.name)
                continue

            if location.item.player == self.player:
                print("Adding item: " + str(location.item.code) + "to " + location.name)
                items_id.append(location.item.code)
                items_address.append(name_to_dw_code[location.item.name])

            if location.player == self.player:
                locations_address.append(item_dictionary[location_dictionary[location.name].default_item].dw_code)
                locations_id.append(location.address)
                print("Adding item: " + str(item_dictionary[location_dictionary[location.name].default_item].dw_code) + "to " + location.name)
                if location.item.player == self.player:
                    locations_target.append(name_to_dw_code[location.item.name])
                else:
                    locations_target.append(0)

        slot_data = {
            "options": {
                "guaranteed_items": self.multiworld.guaranteed_items[self.player].value,
                "exp_multiplier": self.multiworld.exp_multiplier[self.player].value,
                "progressive_stats": self.multiworld.progressive_stats[self.player].value,
                "random_starter": self.multiworld.random_starter[self.player].value
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
