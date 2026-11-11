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

        // Stored in the unused tail of the PS1 save-file block (SAVE_FILE + 0x1900, RAM 0x8013322C).
        // int32, written by the client, persisted with every save, zeroed by the game on new game
        // and restored on load. See dw_decomp PATCH_MEMORY_MAP.md "Save File Layout".
        public static ulong ItemReceivedIndex = 0x0013322C;

        // Recruit "soul" flags: trigger 1024+digimonId, stored as a bitfield in the save-file tail
        // (SAVE_FILE + 0x1980, RAM 0x801332AC; byte id/8, bit id%8). A recruitable digimon only
        // appears in the world once its soul bit is set; the client sets it when the
        // "<Digimon> Soul" item arrives. The digimon id comes from the recruit's done flag
        // (Locations.json address/bit = trigger 720+id). Zeroed by the game on new game.
        public static ulong SoulFlagsBase = 0x001332AC;
        public static ulong TriggerBitsBase = 0x001BDFCD;   // ScriptState.triggers (800 bits)
        public static int RecruitDoneFlagBase = 720;

        // Booster pack flags: one byte in the save-file tail (SAVE_FILE + 0x1A20, RAM 0x8013334C),
        // bit = pack flag = item id - BoosterPackItemBase. The card shop lists a pack once its bit is
        // set; the client sets it when the "<Pack> Booster Pack" item arrives. Zeroed on new game.
        public static ulong BoosterPackBits = 0x0013334C;
        public static long BoosterPackItemBase = 693003;

        // Custom textbox hook (ROM patch: patch_textbox_hook.py). Data lives in the 8MB extended
        // RAM region (RAM 0x80200000+), so the emulator must run in 8MB mode.
        // Write the SJIS text (terminated by 0D 00 00 00 FE) to the buffer, then write 1 to the
        // request byte. When the script engine is idle the hook starts a real script section on the
        // buffer (it writes SET_DIALOG_OWNER/SHOW_TEXTBOX at 0x200004 in front of the text), sets
        // status to 1, and clears status back to 0 on the first idle frame after the box is gone.
        // Only write a new message while request == 0 and status == 0 (see TextboxQueue).
        public static ulong TextboxRequest = 0x00200000;  // 1 byte: write 1 to trigger
        public static ulong TextboxStatus  = 0x00200001;  // 1 byte: 1 = message in progress, 0 = idle
        public static ulong TextboxHeader  = 0x00200004;  // 4 bytes: written by the hook (1B FF 1A 00)
        public static ulong TextboxBuffer  = 0x00200008;  // 360 bytes: SJIS text + 0D 00 00 00 FE
        public static int   TextboxBufferSize = 360;
    }
}
