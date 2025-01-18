using Archipelago.Core.Util;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DWAP
{
    public class Randomiser
    {
        internal int Seed { get; set; }
        private Random RNG { get; set; }
        public byte Starter { get; set; }
        RandomiserOptions Options { get; set; }
        public Randomiser(RandomiserOptions options)
        {
            Options = options;
            Seed = Options.Seed;
            RNG = new Random(Seed);
        }
        public void Generate()
        {
            // Starter Randomisation
            if(Options.StarterRandomisation == StarterRandomisation.RookieOnly)
            {
                Starter = (byte)Helpers.GetRookieNum(RNG.Next(0, 8));
            }
            else if(Options.StarterRandomisation == StarterRandomisation.All)
            {
                Starter = (byte)RNG.Next(1, 65);
            }


        }

        public List<DigimonTechniqueData> ShuffleAndWriteTechniques(List<DigimonTechniqueData> techniques)
        {
            int n = techniques.Count;
            while (n > 1)
            {
                n--;
                int k = RNG.Next(n + 1);
                DigimonTechniqueData temp = techniques[k];
                techniques[k] = techniques[n];
                techniques[n] = temp;
            }

            var currentAddress = Addresses.TechniqueStartAddress;
            var learningChanceAddress = Addresses.LearningChanceStartAddress;

            foreach (var tech in techniques)
            {
                Memory.WriteByte(currentAddress, tech.Unknown1);
                Memory.WriteByte(currentAddress + Addresses.ByteOffset, tech.Unknown2);
                Memory.Write(currentAddress + 2 * Addresses.ByteOffset, tech.AITargetDistance);
                Memory.Write(currentAddress + 2 * Addresses.ByteOffset + Addresses.ShortOffset, tech.Power);
                Memory.WriteByte(currentAddress + 2 * Addresses.ByteOffset + 2 * Addresses.ShortOffset, tech.MP);
                Memory.WriteByte(currentAddress + 3 * Addresses.ByteOffset + 2 * Addresses.ShortOffset, tech.IFrames);
                Memory.WriteByte(currentAddress + 4 * Addresses.ByteOffset + 2 * Addresses.ShortOffset, tech.Range);
                Memory.WriteByte(currentAddress + 5 * Addresses.ByteOffset + 2 * Addresses.ShortOffset, tech.Type);
                Memory.WriteByte(currentAddress + 6 * Addresses.ByteOffset + 2 * Addresses.ShortOffset, tech.StatusEffect);
                Memory.WriteByte(currentAddress + 7 * Addresses.ByteOffset + 2 * Addresses.ShortOffset, tech.BlockingFactor);
                Memory.WriteByte(currentAddress + 8 * Addresses.ByteOffset + 2 * Addresses.ShortOffset, tech.StatusChance);
                Memory.WriteByte(currentAddress + 9 * Addresses.ByteOffset + 2 * Addresses.ShortOffset, tech.Unknown3);
                Memory.WriteByte(currentAddress + 10 * Addresses.ByteOffset + 2 * Addresses.ShortOffset, tech.Unknown4);
                Memory.WriteByte(currentAddress + 11 * Addresses.ByteOffset + 2 * Addresses.ShortOffset, tech.Unknown5);
                Memory.WriteByte(learningChanceAddress, tech.LearningChance1);
                Memory.WriteByte(learningChanceAddress + Addresses.ByteOffset, tech.LearningChance2);
                Memory.WriteByte(learningChanceAddress + 2 * Addresses.ByteOffset, tech.LearningChance3);

                currentAddress += 12 * Addresses.ByteOffset + 2 * Addresses.ShortOffset;
                learningChanceAddress += 3 * Addresses.ByteOffset;
            }
            return techniques;
        }
    }
}
