using Archipelago.Core;
using Archipelago.Core.Models;
using Archipelago.Core.Util;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
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
        public static List<Location> GetLocations()
        {
            var json = OpenEmbeddedResource("DWAP.Resources.Locations.json");
            var list = JsonConvert.DeserializeObject<List<Location>>(json);
            return list;
        }
        public static List<DigimonItem> GetConsumables()
        {
            var json = OpenEmbeddedResource("DWAP.Resources.DigimonItems.json");
            var list = JsonConvert.DeserializeObject<List<DigimonItem>>(json);
            return list;
        }
        public static List<DigimonWorldItem> GetDigimonSouls()
        {
            var json = OpenEmbeddedResource("DWAP.Resources.DigimonSouls.json");
            var list = JsonConvert.DeserializeObject<List<DigimonWorldItem>>(json);
            foreach(var item in list)
            {
                item.Type = ItemType.Soul;
            }
            return list;
        }
        public static List<Location> GetDigimonCards()
        {
            var json = OpenEmbeddedResource("DWAP.Resources.DigimonCards.json");
            var list = JsonConvert.DeserializeObject<List<Location>>(json);
            return list;
        }
        public static List<Location> GetProsperityLocations()
        {
            var json = OpenEmbeddedResource("DWAP.Resources.Prosperity.json");
            var list = JsonConvert.DeserializeObject<List<Location>>(json);
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
        public static ulong GetDuckstationOffset()
        {
            var baseAddress = Memory.GetBaseAddress("duckstation-qt-x64-ReleaseLTCG");
            var offset = Memory.ReadULong(baseAddress + 0x008C4FA8);
            return offset;
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
            var completedLocations = state.CompletedLocations.Where(x => x.Name.ToLower().Contains("recruited"));

            var digimonNames = completedLocations.Select(x => x.Name.Replace(" Recruited", ""));
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
            foreach (var digimon in digimonNames)
            {
                if (rookieList.Contains(digimon))
                {
                    result += 1;
                }
                else if (championList.Contains(digimon))
                {
                    result += 2;
                }
                else if(ultimateList.Contains(digimon))
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

