using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DWAP
{
    public class Addresses
    {
        public const uint ePSXEOffset = 0x00A579A0;

        public const uint ByteOffset = 0x00000001;
        public const uint ShortOffset = 0x00000002;
        public const uint IntOffset = 0x00000004;
        public const uint TechniqueOffset = 12 * ByteOffset + 2 * ShortOffset;

        public const uint LastScript = ePSXEOffset + 0x00134FDC;
        public const uint MaxHp = ePSXEOffset + 0x001557F0;
        public const uint MaxMp = ePSXEOffset + 0x001557F2;
        public const uint CurrentOffense = ePSXEOffset + 0x001557E0;
        public const uint CurrentDefence = ePSXEOffset + 0x001557E2;
        public const uint CurrentSpeed = ePSXEOffset + 0x001557E4;
        public const uint CurrentBrains = ePSXEOffset + 0x001557E6;
        public const uint InventorySize = ePSXEOffset + 0x000DD4CE;
        public const uint ItemBankBaseAddress = ePSXEOffset + 0x001BDF2C;
        public const uint CurrentBits = ePSXEOffset + 0x00134EB8;

        public const uint Starter1 = ePSXEOffset + 0x000EE9D8;
        public const uint Starter2 = ePSXEOffset + 0x000EE9D0;

        public const uint TechniqueSlot1 = ePSXEOffset + 0x001557EC;

        public const uint TechniqueStartAddress = ePSXEOffset + 0x0012623C;
        public const uint LearningChanceStartAddress = ePSXEOffset + 0x00125FA4;

        public const uint MonochromeProfitAddress = ePSXEOffset + 0x0013500C;

        public const uint CardStartAddress = ePSXEOffset + 0x001bdfac;

        public const uint ChartStartAddress = ePSXEOffset + 0x001be00d;
        //public const uint LastScript = 0x00B8C97C;
        //public const uint MaxHp = 0x00BAD190;
        //public const uint MaxMp = 0x00BAD192;
        //public const uint CurrentOffense = 0x00BAD180;
        //public const uint CurrentDefence = 0x00BAD182;
        //public const uint CurrentSpeed = 0x00BAD184;
        //public const uint CurrentBrains = 0x00BAD186;
        //public const uint InventorySize = 0x00B94E6E;
        //public const uint ItemBankBaseAddress = 0x00C158CC;
        //public const uint CurrentBits = 0x00B8C858;

        //public const uint Starter1 = 0x00B46378;
        //public const uint Starter2 = 0x00B46370;

        //public const uint TechniqueSlot1 = 0x00BAD18C;

        //public const uint TechniqueStartAddress = 0x00B7DBDC;
        //public const uint LearningChanceStartAddress = 0x00B7D944;
    }
}
