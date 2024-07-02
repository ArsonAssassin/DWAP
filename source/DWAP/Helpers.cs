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
        public static List<DigimonWorldItem> GetItems()
        {
            var json = OpenEmbeddedResource("DWAP.Resources.Items.json");
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
    }
}

