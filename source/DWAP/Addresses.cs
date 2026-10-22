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
        public static ulong InventorySize = 0x000DD4CE; //0x00B94E6E?
        public static ulong ItemBankBaseAddress = 0x001BDF2C; //0x00C158CC?
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

        // Offset between event-completion flags (720+id) and town-presence flags (200+id)
        // New event flags are 65 bytes (520 triggers / 8) higher in the trigger bitfield
        public static ulong EventToTownFlagOffset = 0x41;

        public static ulong CardStartAddress = 0x001bdfac;

        public static ulong ChartStartAddress = 0x001be00d;
        public static ulong ProsperityPoints = 0x001BE032;

        public static ulong RecruitmentFunctionAddress = 0x00000000;

        // Stored in PS1 save data, after the event-completion flags (last at 0x001BE02E bit 2)
        // 2 bytes for a ushort to track item received index for crash recovery
        public static ulong ItemReceivedIndex = 0x001BE02F;

        // Custom textbox hook (ROM patch: patch_textbox_hook.py)
        // Write 1 to trigger; routine clears it and sets status to 1 while showing
        public static ulong TextboxRequest = 0x0007C98C;  // 1 byte: write 1 to trigger
        public static ulong TextboxStatus  = 0x0007C98D;  // 1 byte: 0=idle, 1=showing
        public static ulong TextboxBuffer  = 0x0007C990;  // ~364 bytes: SJIS text data
    }
}
