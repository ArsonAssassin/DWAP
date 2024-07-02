using Archipelago.ePSXe.Util;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DWAP
{
    public class Recruitment
    {
        [JsonConverter(typeof(HexToIntConverter))]
        public int Address { get; set; }
        public int AddressBit { get; set; }
        public string Name { get; set; }
        public bool IsRecruited { get; set; }
    }
}
