using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DWAP.RomPatcher
{
    [DigimonWorldDataFormat("<BxBB")]
    public class TokomonItem : IDigimonWorldDataStructure
    {
        [BinaryField(0)]
        public byte Cmd { get; set; }

        [BinaryField(2)]
        public byte Item { get; set; }

        [BinaryField(3)]
        public byte Count { get; set; }
    }
}
