using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DWAP.Models
{
    public class DigimonTechniqueData
    {
        public string Name { get; set; }
        public int Slot { get; set; }
        public byte Unknown1 { get; set; }
        public byte Unknown2 { get; set; }
        public short AITargetDistance { get; set; }
        public short Power { get; set; }
        public byte MP { get; set; }
        public byte IFrames { get; set; }
        public byte Range { get; set; }
        public byte Type { get; set; }
        public byte StatusEffect { get; set; }
        public byte BlockingFactor { get; set; }
        public byte StatusChance { get; set; }
        public byte Unknown3 { get; set; }
        public byte Unknown4 { get; set; }
        public byte Unknown5 { get; set; }
        public byte LearningChance1 { get; set; }
        public byte LearningChance2 { get; set; }
        public byte LearningChance3 { get; set; }

        public uint Address { get; set; }
        public int AddressBit { get; set; }
    }
}
