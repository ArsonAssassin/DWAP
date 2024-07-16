using Archipelago.ePSXe.Models;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

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
        public static List<Location> GetTemp()
        {
            var json = OpenEmbeddedResource("DWAP.Resources.temp.json");
            var list = JsonConvert.DeserializeObject<List<Location>>(json);
            return list;
        }
        public static List<DigimonWorldItem> GetItems()
        {
            var json = OpenEmbeddedResource("DWAP.Resources.APItems.json");
            var list = JsonConvert.DeserializeObject<List<DigimonWorldItem>>(json);
            return list;
        }
        public static List<Recruitment> GetRecruitment()
        {
            var json = OpenEmbeddedResource("DWAP.Resources.Recruitment.json");
            var list = JsonConvert.DeserializeObject<List<Recruitment>>(json);
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

