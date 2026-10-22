# world/dw1/__init__.py
import os
import pkgutil
from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification
from Options import Toggle

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule

from .Items import DigimonWorldItem, DigimonWorldItemCategory, item_dictionary, key_item_names, key_item_categories, item_descriptions, _all_items, BuildItemPool
from .Locations import DigimonWorldLocation, DigimonWorldLocationCategory, location_tables, location_dictionary
from .Options import DigimonWorldOption
from .Patch import DW1ProcedurePatch, DW1Settings
from .RecruitDigimon import recruit_digimon_list

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
    settings_key = "dw1_settings"
    settings: DW1Settings  # type: ignore
    data_version = 0
    base_id = 690000
    enabled_location_categories: Set[DigimonWorldLocationCategory]
    required_client_version = (0, 6, 2)
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
        if self.options.include_card_locations.value:
            self.enabled_location_categories.add(DigimonWorldLocationCategory.CARD)
        if self.options.include_chest_locations.value:
            self.enabled_location_categories.add(DigimonWorldLocationCategory.CHEST)
        


    def create_regions(self):
        # Create Regions
        regions: Dict[str, Region] = {}
        regions["Menu"] = self.create_region("Menu", [])
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
            "Start Game", "Cards",
            "Prosperity",
            "File City", "Native Forest", "Drill Tunnel", "Lava Cave - Hot", "Lava Cave - Cooled",
            "Gear Savanna", "Tropical Jungle", "Ancient Dino Region",
            "Freezeland", "Great Canyon", "Ogre Fortress", "Grey Lords Mansion",
            "Underground Lab", "Factorial Town", "Misty Trees", "Toy Town",
            "Ice Sanctuary", "Mt Infinity", "Back Dimension", "Mt Panorama",
            "Secret Beach Cave", "Leomon Cave", "Beetle Land", "Nanimon",
        ]})

        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{from_region} -> {to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])

        create_connection("Menu", "Start Game")
        create_connection("Start Game", "Prosperity")

        # Geographic regions — flat graph for now (all from File City)
        create_connection("Start Game", "File City")
        
        create_connection("Start Game", "Nanimon")
        
        create_connection("File City", "Native Forest")
        create_connection("File City", "Factorial Town")        
        create_connection("File City", "Mt Infinity")           
        create_connection("File City", "Cards")       
        
        create_connection("Native Forest", "Tropical Jungle")
        create_connection("Native Forest", "Drill Tunnel")
        create_connection("Native Forest", "Mt Panorama")
        create_connection("Native Forest", "Beetle Land")

        create_connection("Drill Tunnel", "Lava Cave - Hot")
        create_connection("Drill Tunnel", "Lava Cave - Cooled")
        create_connection("Drill Tunnel", "Leomon Cave")
        create_connection("Lava Cave - Cooled", "Mt Panorama")

        create_connection("Tropical Jungle", "Ancient Dino Region")
        create_connection("Tropical Jungle", "Great Canyon")
        create_connection("Tropical Jungle", "Grey Lords Mansion")
        
        create_connection("Great Canyon", "Ogre Fortress")
        create_connection("Great Canyon", "Freezeland")
       
        create_connection("Mt Panorama", "Gear Savanna")       
        
        create_connection("Gear Savanna", "Misty Trees")      
        create_connection("Gear Savanna", "Cards")       
        
        create_connection("Factorial Town", "Gear Savanna")
        
        create_connection("Misty Trees", "Freezeland")
        create_connection("Misty Trees", "Toy Town")
        
        create_connection("Freezeland", "Secret Beach Cave")
        create_connection("Freezeland", "Ice Sanctuary")        
        
        create_connection("Grey Lords Mansion", "Underground Lab")
        
        create_connection("Grey Lords Mansion", "Back Dimension")
        create_connection("Ice Sanctuary", "Back Dimension")
        create_connection("Ogre Fortress", "Back Dimension")
        
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
            if item.category == DigimonWorldItemCategory.RECRUIT:
                itempool.append(self.create_item(item.name))
                itempoolSize -= 1
            
        
        print(f"Itempool size after adding recruits: {itempoolSize}")
        filler_pool = BuildItemPool(self.multiworld, itempoolSize, self.options)
        for item in filler_pool:
            itempool.append(self.create_item(item.name))
            itempoolSize -= 1
        print(f"Itempool size after adding fillers: {itempoolSize}")

        if self.options.early_statcap.value:
            # print("Adding early stat cap item")
            location = self.multiworld.get_location("Start Game", self.player)
            location.place_locked_item(self.create_item("Progressive Stat Cap"))
        # Add regular items to itempool
        print("Final itempool order:")
        for i, item in enumerate(itempool[:20]):
            print(f"  {i}: {item.name}")
        self.multiworld.itempool += itempool
        
    def create_item(self, name: str) -> Item:
        useful_categories = {
           DigimonWorldItemCategory.CONSUMABLE,
           DigimonWorldItemCategory.DV,
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
        def calculate_prosperity(self, state, current_digimon = None) -> int:
            current_prosperity = 0
            for digimon in recruit_digimon_list:
                if state.has(digimon.name, self.player):
                    current_prosperity += digimon.prosperity_value
            return current_prosperity

        def has_minimum_statcap(self, state, count) -> bool:
            return state.has("Progressive Stat Cap", self.player, count)

        def set_indirect_rule(self, regionName, entrance, rule):
            region = self.multiworld.get_region(regionName, self.player)
            location = self.multiworld.get_location(regionName, self.player)
            set_rule(location, rule)
            self.multiworld.register_indirect_condition(region, entrance)

        def build_digimon_rule(d, world):
            def rule(state):
                if d.min_statcap > 0 and not has_minimum_statcap(world, state, d.min_statcap):
                    return False
                for req in d.digimon_requirements:
                    if not state.has(req, self.player):
                        return False
                if d.or_digimon_requirements:
                    if not any(state.has(req, self.player) for req in d.or_digimon_requirements):
                        return False
                if calculate_prosperity(world, state, d.name) < d.prosperity_requirement:
                     return False
                return True
            return rule
        def shop_level(self, state) -> int:
            shopLevel = 0
            if state.has("Monochromon", self.player):
                shopLevel += 1
            if state.has("Patamon", self.player):
                shopLevel += 1
            if state.has("Biyomon", self.player):
                shopLevel += 1
            if state.has("Unimon", self.player):
                shopLevel += 1
            return shopLevel
                
        if self.options.goal.value == 0:
            self.multiworld.completion_condition[self.player] = lambda state, s=self: calculate_prosperity(s, state) >= 100
        else:
            self.multiworld.completion_condition[self.player] = lambda state, s=self: state.can_reach_location("Digitamamon", s.player)

        set_rule(self.multiworld.get_location("Start Game", self.player), lambda state, s=self: True)
        set_rule(self.multiworld.get_entrance("Menu -> Start Game", self.player), lambda state, s=self: True)
        set_rule(self.multiworld.get_entrance("File City -> Cards", self.player), lambda state, s=self:  shop_level(s, state) >=3)
        set_rule(self.multiworld.get_entrance("Gear Savanna -> Cards", self.player), lambda state, s=self: True)
        set_rule(self.multiworld.get_entrance("Start Game -> Prosperity", self.player), lambda state, s=self: True)
        set_rule(self.multiworld.get_entrance("Start Game -> File City", self.player), lambda state, s=self: True)
        set_rule(self.multiworld.get_entrance("Start Game -> Nanimon", self.player), lambda state, s=self: True)
        set_rule(self.multiworld.get_entrance("File City -> Native Forest", self.player), lambda state, s=self: state.can_reach_location("Agumon", s.player))
        set_rule(self.multiworld.get_entrance("File City -> Factorial Town", self.player), lambda state, s=self: state.can_reach_location("Whamon", s.player))
        set_rule(self.multiworld.get_entrance("File City -> Mt Infinity", self.player), lambda state, s=self: calculate_prosperity(s, state) >= 50)
        set_rule(self.multiworld.get_entrance("Native Forest -> Tropical Jungle", self.player), lambda state, s=self: state.can_reach_location("Agumon", s.player))
        set_rule(self.multiworld.get_entrance("Native Forest -> Drill Tunnel", self.player), lambda state, s=self: True)
        set_rule(self.multiworld.get_entrance("Native Forest -> Mt Panorama", self.player), lambda state, s=self: state.has("Landslide blocking path to Unimon cleared", s.player))
        set_rule(self.multiworld.get_entrance("Native Forest -> Beetle Land", self.player), lambda state, s=self: state.can_reach_location("Seadramon", s.player))
        set_rule(self.multiworld.get_entrance("Drill Tunnel -> Lava Cave - Hot", self.player), lambda state, s=self: state.has("Lava Cave opened", s.player))
        set_rule(self.multiworld.get_entrance("Drill Tunnel -> Lava Cave - Cooled", self.player), lambda state, s=self: state.can_reach_location("Meramon", s.player))
        set_rule(self.multiworld.get_entrance("Lava Cave - Cooled -> Mt Panorama", self.player), lambda state, s=self: state.has("Back Exit for Drill Tunnel opened", s.player))
        set_rule(self.multiworld.get_entrance("Drill Tunnel -> Leomon Cave", self.player), lambda state, s=self: calculate_prosperity(s, state) >= 45)
        set_rule(self.multiworld.get_entrance("Tropical Jungle -> Ancient Dino Region", self.player), lambda state, s=self: state.can_reach_location("Centarumon", s.player))
        set_rule(self.multiworld.get_entrance("Tropical Jungle -> Great Canyon", self.player), lambda state, s=self: state.has("Yuramon told you about the Invisible Bridge", s.player))
        set_rule(self.multiworld.get_entrance("Tropical Jungle -> Grey Lords Mansion", self.player), lambda state, s=self: True)
        set_rule(self.multiworld.get_entrance("Great Canyon -> Ogre Fortress", self.player), lambda state, s=self: True)
        set_rule(self.multiworld.get_entrance("Great Canyon -> Freezeland", self.player), lambda state, s=self: True)
        set_rule(self.multiworld.get_entrance("Mt Panorama -> Gear Savanna", self.player), lambda state, s=self: True)
        set_rule(self.multiworld.get_entrance("Gear Savanna -> Misty Trees", self.player), lambda state, s=self: True)
        set_rule(self.multiworld.get_entrance("Factorial Town -> Gear Savanna", self.player), lambda state, s=self: state.can_reach_location("Andromon", s.player))
        set_rule(self.multiworld.get_entrance("Misty Trees -> Freezeland", self.player), lambda state, s=self: True)
        set_rule(self.multiworld.get_entrance("Misty Trees -> Toy Town", self.player), lambda state, s=self: True)
        set_rule(self.multiworld.get_entrance("Freezeland -> Secret Beach Cave", self.player), lambda state, s=self: True)
        set_rule(self.multiworld.get_entrance("Freezeland -> Ice Sanctuary", self.player), lambda state, s=self: True)
        set_rule(self.multiworld.get_entrance("Grey Lords Mansion -> Underground Lab", self.player), lambda state, s=self: state.has("Shellmon", s.player))
        set_rule(self.multiworld.get_entrance("Grey Lords Mansion -> Back Dimension", self.player), lambda state, s=self: state.can_reach_location("Digitamamon", s.player))
        set_rule(self.multiworld.get_entrance("Ice Sanctuary -> Back Dimension", self.player), lambda state, s=self: state.can_reach_location("Digitamamon", s.player))
        set_rule(self.multiworld.get_entrance("Ogre Fortress -> Back Dimension", self.player), lambda state, s=self: state.can_reach_location("Digitamamon", s.player))

        for digimon in recruit_digimon_list:
            location = self.multiworld.get_location(digimon.name, self.player)
            set_rule(location, build_digimon_rule(digimon, self))
            region = location.parent_region
            for entrance in region.entrances:
                self.multiworld.register_indirect_condition(region, entrance)

        for card in [card for card in self.multiworld.get_locations(self.player) if card.category == DigimonWorldLocationCategory.CARD]:            
            if(card.name == "Machinedramon Card"):
                set_rule(card, lambda state, s=self: state.has("Digitamamon", s.player) and calculate_prosperity(s, state) >= 50)
                continue
            set_rule(card, lambda state, s=self: True)

        # Event flag rules
        set_rule(self.multiworld.get_location("Will get ambushed by Greymon in File City", self.player),
            lambda state, s=self: calculate_prosperity(s, state) >= 15)
        set_rule(self.multiworld.get_location("Yuramon told you about the Invisible Bridge", self.player),
            lambda state, s=self: calculate_prosperity(s, state) >= 6)
        set_rule(self.multiworld.get_location("Landslide blocking path to Unimon cleared", self.player),
            lambda state, s=self: state.can_reach_location("Meramon", s.player))
        set_rule(self.multiworld.get_location("Lava Cave opened", self.player),
            lambda state, s=self: True)
        set_rule(self.multiworld.get_location("Back Exit for Drill Tunnel opened", self.player),
            lambda state, s=self: state.can_reach_location("Drimogemon", s.player))
        set_rule(self.multiworld.get_location("Unlocked Amazing Rod", self.player),
            lambda state, s=self: state.has("Path to Volume Villa has been opened", s.player))
        set_rule(self.multiworld.get_location("Defeated Ogremon #1", self.player),
            lambda state, s=self: True)
        set_rule(self.multiworld.get_location("Beat Ogremon #2", self.player),
            lambda state, s=self: state.has("Defeated Ogremon #1", s.player))
        set_rule(self.multiworld.get_location("Beaten Ogremon #3", self.player),
            lambda state, s=self: state.has("Beat Ogremon #2", s.player))
        set_rule(self.multiworld.get_location("Shellmon's island is elevated", self.player),
            lambda state, s=self: state.has("Beat Ogremon #2", s.player))
        set_rule(self.multiworld.get_location("Shellmon's island is down again", self.player),
            lambda state, s=self: state.has("Beat Ogremon #2", s.player))
        set_rule(self.multiworld.get_location("Talked with Shellmon about the elevator problem", self.player),
            lambda state, s=self: state.has("Beat Ogremon #2", s.player))
        set_rule(self.multiworld.get_location("Factorial Town (Savanna) entrance opened", self.player),
            lambda state, s=self: state.can_reach_location("Andromon", s.player))
        set_rule(self.multiworld.get_location("Factorial Town entrance open", self.player),
            lambda state, s=self: state.can_reach_location("Andromon", s.player))

        # Additional location rules using events
        add_rule(self.multiworld.get_location("Greymon", self.player),
            lambda state, s=self: state.has("Will get ambushed by Greymon in File City", s.player))
        add_rule(self.multiworld.get_location("Ogremon", self.player),
            lambda state, s=self: state.has("Beaten Ogremon #3", s.player))
        add_rule(self.multiworld.get_location("Chest: Secret Beach Cave", self.player),
            lambda state, s=self: state.has("Beaten Ogremon #3", s.player))
        add_rule(self.multiworld.get_location("Seadramon", self.player),
            lambda state, s=self: state.has("Unlocked Amazing Rod", s.player))

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
                "goal": self.options.goal.value,
                "required_prosperity": self.options.required_prosperity.value,
                "guaranteed_items": self.options.guaranteed_items.value,
                "exp_multiplier": self.options.exp_multiplier.value,
                "progressive_stats": self.options.progressive_stats.value,
                "random_starter": self.options.random_starter.value,
                "early_statcap": self.options.early_statcap.value,
                "random_techniques": self.options.random_techniques.value,
                "easy_monochromon": self.options.easy_monochromon.value,
                "fast_drimogemon": self.options.fast_drimogemon.value,
                "include_card_locations": self.options.include_card_locations.value,
                "include_chest_locations": self.options.include_chest_locations.value
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

    def generate_output(self, output_directory: str) -> None:
        patch = DW1ProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        patch.write_file("dw1_iso.bsdiff4", pkgutil.get_data(__name__, "data/dw1_iso.bsdiff4"))
        out_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}{DW1ProcedurePatch.patch_file_ending}")
        patch.write(out_path)
