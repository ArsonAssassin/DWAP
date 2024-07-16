using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DWAP.RomPatcher
{
    [DigimonWorldDataFormat("<101s")]
    public class DigimonWorldTextBox : IDigimonWorldDataStructure
    {
        [BinaryField(0)]
        public string data { get; set; }
    }
}
