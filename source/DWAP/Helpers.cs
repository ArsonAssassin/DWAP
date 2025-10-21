using Archipelago.Core;
using Archipelago.Core.Json;
using Archipelago.Core.Models;
using Archipelago.Core.Util;
using Archipelago.Core.Util.GPS;
using DWAP.Models;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

using Location = Archipelago.Core.Models.Location;
namespace DWAP
{
    public static class Helpers
    {
        public static List<ILocation> GetLocations()
        {
            var json = OpenEmbeddedResource("DWAP.Resources.Locations.json");
            var list = LocationJsonHelper.Instance.DeserializeLocations(json);
            return list;
        }
        public static List<DigimonItem> GetConsumables()
        {
            var json = OpenEmbeddedResource("DWAP.Resources.DigimonItems.json");
            var list = JsonConvert.DeserializeObject<List<DigimonItem>>(json);
            return list;
        }
        public static List<ILocation> GetChests()
        {
            var json = OpenEmbeddedResource("DWAP.Resources.Chests.json");
            var list = LocationJsonHelper.Instance.DeserializeLocations(json);
            return list;
        }
        public static List<DigimonWorldItem> GetDigimonSouls()
        {
            var json = OpenEmbeddedResource("DWAP.Resources.DigimonSouls.json");
            var list = JsonConvert.DeserializeObject<List<DigimonWorldItem>>(json);
            foreach (var item in list)
            {
                item.Type = ItemType.Soul;
            }
            return list;
        }
        public static PositionData GetCurrentLocation()
        {
            var currentMapId = Memory.ReadShort(0x00134ffe);
            var dict = DigimonMap();
            var currentMap = dict.SingleOrDefault(x => x.MapId == currentMapId);
            var currentX = Memory.ReadByte(0x000134d56);
            var currentY = Memory.ReadByte(0x000134d55);
            if (currentMap == null)
                return new PositionData() { MapId = currentMapId, MapName = "???", Region = "???", X = currentX, Y = currentY };
            return new PositionData() { MapId = currentMapId, MapName = currentMap.DisplayName, Region = currentMap.Region, X = currentX, Y = currentY };
        }

        public static List<DigimonMap> DigimonMap()
        {
            return new List<DigimonMap>
    {
        new DigimonMap(0, "Toilet", "Native Forest"),
        new DigimonMap(1, "Kunemon's Bed", "Native Forest"),
        new DigimonMap(2, "Palmon's Garden", "Native Forest"),
        new DigimonMap(3, "Etemon's House", "Native Forest"),
        new DigimonMap(4, "Path to beach", "Native Forest"),
        new DigimonMap(5, "Coela Point", "Native Forest"),
        new DigimonMap(6, "Dragon Eye Lake South", "Native Forest"),
        new DigimonMap(7, "Drill Tunnel Entrance", "Native Forest"),
        new DigimonMap(8, "Dragon Eye Lake North", "Native Forest"),
        new DigimonMap(9, "Digimon Bridge", "Native Forest"),
        new DigimonMap(10, "Bridge Path", "Native Forest"),
        new DigimonMap(11, "Bridge", "Jungle"),
        new DigimonMap(12, "Beach", "Jungle"),
        new DigimonMap(13, "Toilet", "Jungle"),
        new DigimonMap(14, "Central Jungle", "Jungle"),
        new DigimonMap(15, "Betamon's Mangrove", "Jungle"),
        new DigimonMap(16, "Amida Entrance", "Jungle"),
        new DigimonMap(17, "Amida Forest", "Jungle"),
        new DigimonMap(18, "Path thru Mt Panorama", "Mt Panorama"),
        new DigimonMap(19, "Mamemon Field", "Mt Panorama"),
        new DigimonMap(20, "Path thru Mt Panorama", "Mt Panorama"),
        new DigimonMap(21, "Unused", "Unknown"),
        new DigimonMap(22, "Toilet", "Mt Panorama"),
        new DigimonMap(23, "Toilet", "Mt Panorama"),
        new DigimonMap(24, "Room 1", "Drill Tunnel"),
        new DigimonMap(25, "Center", "Drill Tunnel"),
        new DigimonMap(26, "Long path", "Drill Tunnel"),
        new DigimonMap(27, "Drimogemon's Kitchen", "Drill Tunnel"),
        new DigimonMap(28, "Underground Pond", "Drill Tunnel"),
        new DigimonMap(29, "Lava Tunnel", "Lava Cave"),
        new DigimonMap(30, "Path", "Lava Cave"),
        new DigimonMap(31, "Meramon's Lair", "Lava Cave"),
        new DigimonMap(32, "Exit", "Lava Cave"),
        new DigimonMap(33, "Chamber", "Lava Cave"),
        new DigimonMap(34, "Overdell", "Great Canyon"),
        new DigimonMap(35, "Cemetary", "Great Canyon"),
        new DigimonMap(36, "Invisible Bridge", "Great Canyon"),
        new DigimonMap(37, "Outside Ogremon Elevator", "Great Canyon"),
        new DigimonMap(38, "Birdramon Elevator", "Great Canyon"),
        new DigimonMap(39, "Shellmon's Island (UP)", "Great Canyon"),
        new DigimonMap(40, "Entrance", "Ogre Fortress"),
        new DigimonMap(41, "Birdramon Elevator (Lower)", "Great Canyon"),
        new DigimonMap(42, "Bottom of Cliff", "Great Canyon"),
        new DigimonMap(43, "Split Path", "Great Canyon"),
        new DigimonMap(44, "Monocrhome Shop Entrance", "Great Canyon"),
        new DigimonMap(45, "Room 1", "Ogre Fortress"),
        new DigimonMap(46, "Room 2", "Ogre Fortress"),
        new DigimonMap(47, "Room 3", "Ogre Fortress"),
        new DigimonMap(48, "Ogremon's Room", "Ogre Fortress"),
        new DigimonMap(49, "Monochrome Shop", "Great Canyon"),
        new DigimonMap(50, "Unused", "Unknown"),
        new DigimonMap(51, "Attic", "Grey Lord Mansion"),
        new DigimonMap(52, "Hall", "Grey Lord Mansion"),
        new DigimonMap(53, "Landing", "Grey Lord Mansion"),
        new DigimonMap(54, "Hallway", "Grey Lord Mansion"),
        new DigimonMap(55, "Dining Room", "Grey Lord Mansion"),
        new DigimonMap(56, "Kitchen", "Grey Lord Mansion"),
        new DigimonMap(57, "Toilet", "Grey Lord Mansion"),
        new DigimonMap(58, "Stairs", "Grey Lord Mansion"),
        new DigimonMap(59, "Chest Room", "Grey Lord Mansion"),
        new DigimonMap(60, "Lab Entrance", "Grey Lord Mansion"),
        new DigimonMap(61, "Unused", "Unknown"),
        new DigimonMap(62, "Bedroom", "Grey Lord Mansion"),
        new DigimonMap(63, "Office", "Grey Lord Mansion"),
        new DigimonMap(64, "Library", "Grey Lord Mansion"),
        new DigimonMap(65, "Unused", "Unknown"),
        new DigimonMap(66, "Basement", "Grey Lord Mansion"),
        new DigimonMap(67, "Lab Passage", "Grey Lord Mansion"),
        new DigimonMap(68, "Lab Entrance", "Grey Lord Mansion"),
        new DigimonMap(69, "Entrance", "Gear Savanna"),
        new DigimonMap(70, "Factorial Approach", "Gear Savanna"),
        new DigimonMap(71, "Factorial Door", "Gear Savanna"),
        new DigimonMap(72, "Patamon Clearing", "Gear Savanna"),
        new DigimonMap(73, "Hide n Seek", "Gear Savanna"),
        new DigimonMap(74, "Vending Machine", "Gear Savanna"),
        new DigimonMap(75, "Recycling Shop", "Gear Savanna"),
        new DigimonMap(76, "Leomon Cutscene", "Gear Savanna"),
        new DigimonMap(77, "Toilet", "Gear Savanna"),
        new DigimonMap(78, "Leomon's Gym", "Gear Savanna"),
        new DigimonMap(79, "Toilet", "Glacial Region"),
        new DigimonMap(80, "Entrance", "Glacial Region"),
        new DigimonMap(81, "Vending Machine", "Glacial Region"),
        new DigimonMap(82, "Doorway", "Glacial Region"),
        new DigimonMap(83, "Entrance", "Speedy Region"),
        new DigimonMap(84, "Bone Tunnel", "Speedy Region"),
        new DigimonMap(85, "Hint Area", "Speedy Region"),
        new DigimonMap(86, "Landing Site", "Speedy Region"),
        new DigimonMap(87, "Secret Passage", "Speedy Region"),
        new DigimonMap(88, "Entrance", "Freezeland"),
        new DigimonMap(89, "Approach", "Freezeland"),
        new DigimonMap(90, "Toilet", "Freezeland"),
        new DigimonMap(91, "Ice Sanctuary Path", "Freezeland"),
        new DigimonMap(92, "Outside Ice Sanctuary", "Freezeland"),
        new DigimonMap(93, "Center", "Freezeland"),
        new DigimonMap(94, "Igloo", "Freezeland"),
        new DigimonMap(95, "Garurumon Clearing", "Freezeland"),
        new DigimonMap(96, "Beach", "Freezeland"),
        new DigimonMap(97, "Entrance", "Ice Sanctuary"),
        new DigimonMap(98, "Hallway", "Ice Sanctuary"),
        new DigimonMap(99, "Gym", "Ice Sanctuary"),
        new DigimonMap(100, "Path", "Ice Sanctuary"),
        new DigimonMap(101, "Teleporter Room 1", "Ice Sanctuary"),
        new DigimonMap(102, "Unknown", "Ice Sanctuary"),
        new DigimonMap(103, "Teleporter Room 2", "Ice Sanctuary"),
        new DigimonMap(104, "Machinedramon", "Back Dimension"),
        new DigimonMap(105, "Entrance", "Beetle Land"),
        new DigimonMap(106, "Center", "Beetle Land"),
        new DigimonMap(107, "Kabuterimon Gym", "Beetle Land"),
        new DigimonMap(108, "Kuwagamon Gym", "Beetle Land"),
        new DigimonMap(109, "Entrance", "Native Forest"),
        new DigimonMap(110, "Panorama Approach (Blocked)", "Native Forest"),
        new DigimonMap(111, "Panorama Approach (Open)", "Native Forest"),
        new DigimonMap(112, "Green Gym", "Native Forest"),
        new DigimonMap(113, "Statue Room", "Leomon Ancestor Cave"),
        new DigimonMap(114, "Entrance", "Leomon Ancestor Cave"),
        new DigimonMap(115, "Entrance", "Misty Trees"),
        new DigimonMap(116, "Shellmon", "Misty Trees"),
        new DigimonMap(117, "Kokatorimon", "Misty Trees"),
        new DigimonMap(118, "Passage", "Misty Trees"),
        new DigimonMap(119, "Cherrymon", "Misty Trees"),
        new DigimonMap(120, "Gabumon", "Misty Trees"),
        new DigimonMap(121, "Freezeland Exit", "Misty Trees"),
        new DigimonMap(122, "Path (cooled)", "Lava Cave"),
        new DigimonMap(123, "Lower (cooled)", "Lava Cave"),
        new DigimonMap(124, "Meramon (cooled)", "Lava Cave"),
        new DigimonMap(125, "Demimeramon (cooled)", "Lava Cave"),
        new DigimonMap(126, "Long Corridor", "Drill Tunnel"),
        new DigimonMap(127, "Shellmon Island (DOWN)", "Great Canyon"),
        new DigimonMap(128, "Split Path (Ogremon Defeated)", "Great Canyon"),
        new DigimonMap(129, "Birdramon's Nest", "Great Canyon"),
        new DigimonMap(130, "Storage Room", "Ogre Fortress"),
        new DigimonMap(131, "Recycle Shop (With Shop)", "Gear Savanna"),
        new DigimonMap(132, "Path to Mojya/Penguinmon", "Freezeland"),
        new DigimonMap(133, "Two Mojyamon", "Freezeland"),
        new DigimonMap(134, "Mojya/Penguinmon Screen", "Freezeland"),
        new DigimonMap(135, "Whamon's Screen", "Freezeland"),
        new DigimonMap(136, "Curling Screen", "Freezeland"),
        new DigimonMap(137, "Frigimon's Igloo", "Freezeland"),
        new DigimonMap(138, "Entrance (Gear Savanna)", "Geko Swamp"),
        new DigimonMap(139, "Toilet", "Geko Swamp"),
        new DigimonMap(140, "Outside", "Volume Villa"),
        new DigimonMap(141, "Inside", "Volume Villa"),
        new DigimonMap(142, "Entrance", "Secret Beach Cave"),
        new DigimonMap(143, "Ogremon Screen", "Secret Beach Cave"),
        new DigimonMap(144, "Main HUB", "Toy Town"),
        new DigimonMap(145, "Monzaemon's Costume", "Custume House"),
        new DigimonMap(146, "Tinmon's House", "Robot House"),
        new DigimonMap(147, "Entrance", "Toy Mansion"),
        new DigimonMap(148, "Second Floor", "Toy Mansion"),
        new DigimonMap(149, "Third Floor", "Toy Mansion"),
        new DigimonMap(150, "Fourth Floor", "Toy Mansion"),
        new DigimonMap(151, "WaruMonzaemon Screen", "Toy Mansion"),
        new DigimonMap(152, "Entrance (Whamon)", "Factorial Town"),
        new DigimonMap(153, "MetalMamemon's Screen", "Factorial Town"),
        new DigimonMap(154, "Main HUB", "Factorial Town"),
        new DigimonMap(155, "Guard Post", "Factorial Town"),
        new DigimonMap(156, "Passage (Gear Savanna)", "Factorial Town"),
        new DigimonMap(157, "Andromon's Room", "Factorial Town"),
        new DigimonMap(158, "HUB (Behind Guards)", "Factorial Town"),
        new DigimonMap(159, "Giromon's Screen (Console intact)", "Factorial Town"),
        new DigimonMap(160, "Giromon's Screen (Console damaged))", "Factorial Town"),
        new DigimonMap(161, "Main Building Entrance", "Factorial Town"),
        new DigimonMap(162, "Remodelling Workshop", "Factorial Town"),
        new DigimonMap(163, "Entrance Screen", "Sewer"),
        new DigimonMap(164, "Entrance Screen", "Trash Mountain"),
        new DigimonMap(165, "Sukamon Screen", "Trash Mountain"),
        new DigimonMap(166, "Level 1", "Mt. Infinity"),
        new DigimonMap(167, "Level 2", "Mt. Infinity"),
        new DigimonMap(168, "Agumon Recruited", "File City Top"),
        new DigimonMap(169, "Palmon Recruited", "File City Top"),
        new DigimonMap(170, "Vegiemon Recruited", "File City Top"),
        new DigimonMap(171, "Birdramon Recruited", "File City Top"),
        new DigimonMap(172, "Birdramon, Palmon Recruited", "File City Top"),
        new DigimonMap(173, "Birdramon, Vegiemon Recruited", "File City Top"),
        new DigimonMap(174, "New House", "File City Top"),
        new DigimonMap(175, "New House, Palmon Recruited", "File City Top"),
        new DigimonMap(176, "New House, Vegiemon Recruited", "File City Top"),
        new DigimonMap(177, "New House, Birdramon Recruited", "File City Top"),
        new DigimonMap(178, "New House, Birdramon, Palmon Recruited", "File City Top"),
        new DigimonMap(179, "New House + Birdramon + Vegiemon Recruited", "File City Top"),
        new DigimonMap(180, "No Recruits", "File City Bottom"),
        new DigimonMap(181, "Shop Unlocked", "File City Bottom"),
        new DigimonMap(182, "Shop, Restaurant Unlocked", "File City Bottom"),
        new DigimonMap(183, "Shop, Restaurant, Clinic Unlocked", "File City Bottom"),
        new DigimonMap(184, "Shop, Restaurant, Clinic, Arena Unlocked", "File City Bottom"),
        new DigimonMap(185, "Shop, Restaurant, Arena Unlocked", "File City Bottom"),
        new DigimonMap(186, "Shop, Arena Unlocked", "File City Bottom"),
        new DigimonMap(187, "Shop, Clinic, Arena Unlocked", "File City Bottom"),
        new DigimonMap(188, "Shop, Arena Unlocked", "File City Bottom"),
        new DigimonMap(189, "Big Shop Unlocked", "File City Bottom"),
        new DigimonMap(190, "Big Shop, Restaurant Unlocked", "File City Bottom"),
        new DigimonMap(191, "Big Shop, Restaurant, Clinic Unlocked", "File City Bottom"),
        new DigimonMap(192, "Big Shop, Restaurant, Clinic, Arena Unlocked", "File City Bottom"),
        new DigimonMap(193, "Big Shop, Restaurant, Arena Unlocked", "File City Bottom"),
        new DigimonMap(194, "Big Shop, Clinic Unlocked", "File City Bottom"),
        new DigimonMap(195, "Big Shop, Clinic, Arena Unlocked", "File City Bottom"),
        new DigimonMap(196, "Big Shop, Arena Unlocked", "File City Bottom"),
        new DigimonMap(197, "Restaurant Unlocked", "File City Bottom"),
        new DigimonMap(198, "Restaurant, Clinic Unlocked", "File City Bottom"),
        new DigimonMap(199, "Restaurant, Clinic, Arena Unlocked", "File City Bottom"),
        new DigimonMap(200, "Restaurant, Arena Unlocked", "File City Bottom"),
        new DigimonMap(201, "Clinic Unlocked", "File City Bottom"),
        new DigimonMap(202, "Clinic, Arena Unlocked", "File City Bottom"),
        new DigimonMap(203, "Arena Unlocked", "File City Bottom"),
        new DigimonMap(204, "No Recruits", "File City Top"),
        new DigimonMap(205, "Expanded Model", "Jijimon's House"),
        new DigimonMap(206, "Second Room", "Jijimon's House"),
        new DigimonMap(207, "Birdra Transport", "Birdra Transport"),
        new DigimonMap(208, "Lobby w/o MetalGreymon/Airdramon", "Arena Lobby"),
        new DigimonMap(209, "Treasure Hunt", "Treasure Hunt"),
        new DigimonMap(210, "Level 3", "Mt. Infinity"),
        new DigimonMap(211, "Item Keeper", "Item Keeper"),
        new DigimonMap(212, "Level 4", "Mt. Infinity"),
        new DigimonMap(213, "Centar Clinic", "Centar Clinic"),
        new DigimonMap(214, "Without Jukebox", "Restaurant"),
        new DigimonMap(215, "With Jukebox", "Restaurant"),
        new DigimonMap(216, "Item Shop", "Item Shop"),
        new DigimonMap(217, "Secret Shop", "Secret Shop"),
        new DigimonMap(218, "Base Model", "Jijimon's House"),
        new DigimonMap(219, "Level 5", "Mt. Infinity"),
        new DigimonMap(220, "Numemon Screen", "Sewer"),
        new DigimonMap(221, "Skullgreymon Screen", "Underground Lab"),
        new DigimonMap(222, "Level 12", "Mt. Infinity"),
        new DigimonMap(223, "Lobby with MetalGreymon/Airdramon", "Arena Lobby"),
        new DigimonMap(224, "Fireplace/Dining Room with Food", "Grey Lord's Mansion"),
        new DigimonMap(225, "Level 13", "Mt. Infinity"),
        new DigimonMap(226, "Level 1", "Back Dimension"),
        new DigimonMap(227, "Level 2", "Back Dimension"),
        new DigimonMap(228, "Level 3", "Back Dimension"),
        new DigimonMap(232, "Second Fireplace/East Wing", "Grey Lord's Mansion"),
        new DigimonMap(233, "Unimon Screen", "Mt. Panorama Spore Area"),
        new DigimonMap(234, "Vademon Screen", "Mt. Panorama Spore Area"),
        new DigimonMap(235, "Curling (Arena)", "Digimon Curling"),
        new DigimonMap(236, "Fianl Cutscene (Old House)", "File City Top"),
        new DigimonMap(237, "Final Cutscene (New House)", "File City Top"),
        new DigimonMap(238, "Initial Cutscene", "File City Top"),
        new DigimonMap(247, "Level 6", "Mt. Infinity"),
        new DigimonMap(248, "Level 7", "Mt. Infinity"),
        new DigimonMap(249, "Level 8", "Mt. Infinity"),
        new DigimonMap(253, "Level 9", "Mt. Infinity"),
        new DigimonMap(254, "Level 10", "Mt. Infinity")
    };
        }
        public static List<ILocation> GetDigimonCards()
        {
            var json = OpenEmbeddedResource("DWAP.Resources.DigimonCards.json");
            var list = LocationJsonHelper.Instance.DeserializeLocations(json);
            return list;
        }
        public static List<ILocation> GetProsperityLocations()
        {
            var json = OpenEmbeddedResource("DWAP.Resources.Prosperity.json");
            var list = LocationJsonHelper.Instance.DeserializeLocations(json);
            return list;
        }
        public static List<DigimonWorldItem> GetAPItems()
        {
            var json = OpenEmbeddedResource("DWAP.Resources.APItems.json");
            var list = JsonConvert.DeserializeObject<List<DigimonWorldItem>>(json);
            return list;
        }
        public static string OpenEmbeddedResource(string resourceName)
        {
            var assembly = Assembly.GetExecutingAssembly();
            using (Stream stream = assembly.GetManifestResourceStream(resourceName))
            using (StreamReader reader = new StreamReader(stream))
            {
                string jsonFile = reader.ReadToEnd();
                return jsonFile;
            }
        }
        public static List<DigimonWorldItem> GetAcquiredSouls(ArchipelagoClient client)
        {
            var list = client.GameState.ReceivedItems.Where(x => x.Id >= 694000 && x.Id <= 694999).Select(x => x.Id).ToList();
            if (!list.Any()) return new List<DigimonWorldItem>();
            var soulLookup = GetDigimonSouls();
            var results = soulLookup.Where(x => list.Contains(x.Id)).ToList();
            if (!results.Any()) return new List<DigimonWorldItem>();
            return results;
        }
        public static List<DigimonWorldItem> GetMissingSouls(ArchipelagoClient client)
        {
            var list = client.GameState.ReceivedItems.Where(x => x.Id >= 694000 && x.Id <= 694999).Select(x => x.Id).ToList();
            var soulLookup = GetDigimonSouls();
            var results = soulLookup.Where(x => !list.Contains(x.Id)).ToList();
            return results;
        }
        public static DigimonTechniqueData PopulateTechData(this DigimonTechniqueData technique)
        {
            technique.Name = LookupTechName(technique.Slot);
            var addressData = GetTechAddress(technique.Slot);
            technique.Address = addressData.Item1;
            technique.AddressBit = addressData.Item2;
            return technique;
        }
        public static int CalculateProsperityPoints(GameState state)
        {
            int result = 0;
            var rookieList = new List<string>()
            {
                "Agumon", "Betamon", "Kunemon", "Palmon", "Gabumon", "Elecmon", "Patamon", "Palmon", "Biyomon", "Sukamon", "Penguinmon", "Nanimon", "Numemon"
            };
            var championList = new List<string>()
            {
                "Bakemon", "Centarumon", "Coelamon", "Greymon", "Monochromon", "Meramon", "Tyrannomon", "Birdramon", "Unimon", "Mojyamon", "Angemon", "Vegiemon",
                "Shellmon", "Whamon", "Frigimon", "Seadramon", "Garurumon", "Kokatorimon", "Ogremon", "Kuwagamon", "Kabuterimon", "Drimogemon", "Ninjamon", "Devimon", "Leomon", "Airdramon"
            };
            var ultimateList = new List<string>()
            {
                "Piximon", "Giromon", "Andromon", "Monzaemon", "Vademon", "MetalMamemon", "SkullGreymon", "Mamemon", "MetalGreymon", "Etemon", "Megadramon", "Digitmamon"
            };
            var list = state.CompletedLocations.GroupBy(x => x.Id).Select(x => x.FirstOrDefault());
            foreach (var location in list)
            {
                if (rookieList.Contains(location.Name))
                {
                    result += 1;
                }
                else if (championList.Contains(location.Name))
                {
                    result += 2;
                }
                else if (ultimateList.Contains(location.Name))
                {
                    result += 3;
                }
            }
            return result;
        }
        private static Tuple<uint, int> GetTechAddress(int slot)
        {
            uint address = 0;
            int bit = 0;

            switch (slot)
            {
                case 0:
                    address = 0x00155800;
                    bit = 0;
                    break;
                case 1:
                    address = 0x00155800;
                    bit = 1;
                    break;
                case 2:
                    address = 0x00155800;
                    bit = 2;
                    break;
                case 3:
                    address = 0x00155800;
                    bit = 3;
                    break;
                case 4:
                    address = 0x00155800;
                    bit = 4;
                    break;
                case 5:
                    address = 0x00155800;
                    bit = 5;
                    break;
                case 6:
                    address = 0x00155800;
                    bit = 6;
                    break;
                case 7:
                    address = 0x00155800;
                    bit = 7;
                    break;
                case 8:
                    address = 0x00155801;
                    bit = 0;
                    break;
                case 9:
                    address = 0x00155801;
                    bit = 1;
                    break;
                case 10:
                    address = 0x00155801;
                    bit = 2;
                    break;
                case 11:
                    address = 0x00155801;
                    bit = 3;
                    break;
                case 12:
                    address = 0x00155801;
                    bit = 4;
                    break;
                case 13:
                    address = 0x00155801;
                    bit = 5;
                    break;
                case 14:
                    address = 0x00155801;
                    bit = 6;
                    break;
                case 15:
                    address = 0x00155801;
                    bit = 7;
                    break;
                case 16:
                    address = 0x00155802;
                    bit = 0;
                    break;
                case 17:
                    address = 0x00155802;
                    bit = 1;
                    break;
                case 18:
                    address = 0x00155802;
                    bit = 2;
                    break;
                case 19:
                    address = 0x00155802;
                    bit = 3;
                    break;
                case 20:
                    address = 0x00155802;
                    bit = 4;
                    break;
                case 21:
                    address = 0x00155802;
                    bit = 5;
                    break;
                case 22:
                    address = 0x00155802;
                    bit = 6;
                    break;
                case 23:
                    address = 0x00155802;
                    bit = 7;
                    break;
                case 24:
                    address = 0x00155803;
                    bit = 0;
                    break;
                case 25:
                    address = 0x00155803;
                    bit = 1;
                    break;
                case 26:
                    address = 0x00155803;
                    bit = 2;
                    break;
                case 27:
                    address = 0x00155803;
                    bit = 3;
                    break;
                case 28:
                    address = 0x00155803;
                    bit = 4;
                    break;
                case 29:
                    address = 0x00155803;
                    bit = 5;
                    break;
                case 30:
                    address = 0x00155803;
                    bit = 6;
                    break;
                case 31:
                    address = 0x00155803;
                    bit = 7;
                    break;
                case 32:
                    address = 0x00155804;
                    bit = 0;
                    break;
                case 33:
                    address = 0x00155804;
                    bit = 1;
                    break;
                case 34:
                    address = 0x00155804;
                    bit = 2;
                    break;
                case 35:
                    address = 0x00155804;
                    bit = 3;
                    break;
                case 36:
                    address = 0x00155804;
                    bit = 4;
                    break;
                case 37:
                    address = 0x00155804;
                    bit = 5;
                    break;
                case 38:
                    address = 0x00155804;
                    bit = 6;
                    break;
                case 39:
                    address = 0x00155804;
                    bit = 7;
                    break;
                case 40:
                    address = 0x00155805;
                    bit = 0;
                    break;
                case 41:
                    address = 0x00155805;
                    bit = 1;
                    break;
                case 42:
                    address = 0x00155805;
                    bit = 2;
                    break;
                case 43:
                    address = 0x00155805;
                    bit = 3;
                    break;
                case 44:
                    address = 0x00155805;
                    bit = 4;
                    break;
                case 45:
                    address = 0x00155805;
                    bit = 5;
                    break;
                case 46:
                    address = 0x00155805;
                    bit = 6;
                    break;
                case 47:
                    address = 0x00155805;
                    bit = 7;
                    break;
                case 48:
                    break;
                case 49:
                    address = 0x00155806;
                    bit = 1;
                    break;
                case 50:
                    address = 0x00155806;
                    bit = 2;
                    break;
                case 51:
                    address = 0x00155806;
                    bit = 3;
                    break;
                case 52:
                    address = 0x00155806;
                    bit = 4;
                    break;
                case 53:
                    address = 0x00155806;
                    bit = 5;
                    break;
                case 54:
                    address = 0x00155806;
                    bit = 6;
                    break;
                case 55:
                    address = 0x00155806;
                    bit = 7;
                    break;
                case 56:
                    address = 0x00155807;
                    bit = 0;
                    break;
                default:
                    break;
            }
            return new Tuple<uint, int>(address, bit);
        }
        public static string LookupTechName(int slot)
        {
            switch (slot)
            {
                case 0: return "Fire Tower";
                case 1: return "Prominence Beam";
                case 2: return "Spit Fire";
                case 3: return "Red Inferno";
                case 4: return "Magma Bomb";
                case 5: return "Heat Laser";
                case 6: return "Inifinity Burn";
                case 7: return "Meltdown";
                case 8: return "Thunder Justice";
                case 9: return "Spinning Shot";
                case 10: return "Electric Cloud";
                case 11: return "Megalo Spark";
                case 12: return "Static Elect";
                case 13: return "Wind Cutter";
                case 14: return "Confused Storm";
                case 15: return "Hurricane";
                case 16: return "Giga Freeze";
                case 17: return "Ice Statue";
                case 18: return "Winter Blast";
                case 19: return "Ice Needle";
                case 20: return "Water Blit";
                case 21: return "Aqua Magic";
                case 22: return "Aurora Freeze";
                case 23: return "Tear Drop";
                case 24: return "Power Crane";
                case 25: return "All Range Beam";
                case 26: return "Metal Sprinter";
                case 27: return "Pulse Laser";
                case 28: return "Delete Program";
                case 29: return "DG Dimension";
                case 30: return "Full Potential";
                case 31: return "Reverse Prog";
                case 32: return "Poison Powder";
                case 33: return "Bug";
                case 34: return "Mass Morph";
                case 35: return "Insect Plague";
                case 36: return "Charm Perfume";
                case 37: return "Poison Claw";
                case 38: return "Danger Sting";
                case 39: return "Green Trap";
                case 40: return "Tremar";
                case 41: return "Muscle Charge";
                case 42: return "War Cry";
                case 43: return "Sonic Jab";
                case 44: return "Dynamite Kick";
                case 45: return "Counter";
                case 46: return "Megaton Punch";
                case 47: return "Buster Dive";
                case 48: return "Dynamite Kick";
                case 49: return "Odor Spray";
                case 50: return "Poop Spd Toss";
                case 51: return "Big Poop Toss";
                case 52: return "Big Rnd Toss";
                case 53: return "Poop Rnd Toss";
                case 54: return "Rnd Spd Toss";
                case 55: return "Horizontal Kick";
                case 56: return "Ult Poop Hell";
                case 57: return "Horizontal Kick";
                case 58: return "Blaze Blast";
                case 59: return "Pepper Breath";
                case 60: return "Lovely Attack";
                case 61: return "Fireball";
                case 62: return "Death Claw";
                case 63: return "Mega Flame";
                case 64: return "Howling Blaster";
                case 65: return "Party time";
                case 66: return "Electric Shock";
                case 67: return "Abduction Beam";
                case 68: return "Smiley Bomb";
                case 69: return "Spnning Needle";
                case 70: return "Spiral Twister";
                case 71: return "Boom Bubble";
                case 72: return "Sweet Breath";
                case 73: return "Bit Bomb";
                case 74: return "Deadly Bomb";
                case 75: return "Drill Spin";
                case 76: return "Electric Thread";
                case 77: return "Energy Bomb";
                case 78: return "Genoside Attack";
                case 79: return "Giga Scissor Claw";
                case 80: return "Dark Shot";
                case 81: return "Pummel Whack";
                case 82: return "Hand of Fate";
                case 83: return "Dark Claw";
                case 84: return "Aerial Attack";
                case 85: return "Bone Boomerang";
                case 86: return "Solar Ray";
                case 87: return "Hydro Pressure";
                case 88: return "Ice Blast";
                case 89: return "Iga School Knife Throw";
                case 90: return "Blasting Spout";
                case 91: return "Fist of the Beast King";
                case 92: return "Dark Network & Concert Crush";
                case 93: return "Electro Shocker";
                case 94: return "Meteor Wing";
                case 95: return "Super Slap";
                case 96: return "Nightmare Syndromer";
                case 97: return "Frozen Fire Shot";
                case 98: return "Poison Ivy";
                case 99: return "Blue Blaster";
                case 100: return "Scissor Claw";
                case 101: return "Super Thunder Strike";
                case 102: return "Spiral Sword";
                case 103: return "Variable Darts";
                case 104: return "Volcanic Strike";
                case 105: return "Subzero Ice Punch";
                case 106: return "Infinity Cannon";
                case 107: return "Party time";
                case 108: return "Party time";
                case 109: return "Crimson Flare";
                case 110: return "Glacial Blast";
                case 111: return "Mail Strome";
                case 112: return "High Electro Shocker";
                case 113:
                case 114:
                case 115:
                case 116:
                case 117:
                case 118:
                case 119:
                case 120:
                    return "Bubble";
                default:
                    return "";
            }
        }

        public static int GetRookieNum(int option)
        {
            switch (option)
            {
                //Agumon
                case 0:
                    return 3;
                //Gabumon
                case 1:
                    return 17;
                //Betamon
                case 2:
                    return 4;
                //Elecmon
                case 3:
                    return 18;
                //Palmon
                case 4:
                    return 46;
                //Patamon
                case 5:
                    return 31;
                //Biyomon
                case 6:
                    return 45;
                //Kunemon
                case 7:
                    return 32;
                //Penguinmon
                case 8:
                    return 57;

                default:
                    return 3;
            }
        }
    }
}

