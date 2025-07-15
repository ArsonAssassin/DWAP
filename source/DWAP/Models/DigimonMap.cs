using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DWAP.Models
{
    public class DigimonMap
    {
        public int MapId { get; set; }
        public string DisplayName { get; set; }
        public string Region { get; set; }
        public DigimonMap(int id, string name, string region)
        {
            MapId = id;
            DisplayName = name;
            Region = region;
        }
    }
}
