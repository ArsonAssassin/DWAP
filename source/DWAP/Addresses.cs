using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DWAP
{
    public class Addresses
    {
        public static ulong ByteOffset = 0x00000001;
        public static ulong ShortOffset = 0x00000002;
        public static ulong IntOffset = 0x00000004;
        public static ulong TechniqueOffset = 12 * ByteOffset + 2 * ShortOffset;

        public static ulong LastScript = 0x00134FDC;
        public static ulong MaxHp = 0x001557F0;
        public static ulong MaxMp = 0x001557F2;
        public static ulong CurrentOffense = 0x001557E0;
        public static ulong CurrentDefence = 0x001557E2;
        public static ulong CurrentSpeed = 0x001557E4;
        public static ulong CurrentBrains = 0x001557E6;
        public static ulong InventorySize = 0x000DD4CE;
        public static ulong ItemBankBaseAddress = 0x001BDF2C;
        public static ulong CurrentBits = 0x00134EB8;

        public static ulong Starter1 = 0x000EE9D8;
        public static ulong Starter2 = 0x000EE9D0;

        public static ulong TechniqueSlot1 = 0x001557EC;

        public static ulong TechniqueStartAddress = 0x0012623C;
        public static ulong LearningChanceStartAddress = 0x00125FA4;

        public static ulong MonochromeProfitAddress = 0x0013500C;
        public static ulong HasBeatenDrimogemon = 0x001BE130;
        public static ulong MeramonTunnel_State = 0x001BE043;
        public static ulong MeramonTunnel_DrimogemonState = 0x001BE042;
        public static ulong MeramonTunnel_DiggingState = 0x001BE04F;

        public static ulong CardStartAddress = 0x001bdfac;

        public static ulong ChartStartAddress = 0x001be00d;
        public static ulong ProsperityPoints = 0x001BE032;
        public static ulong DuckstationOffset;
    }
}
