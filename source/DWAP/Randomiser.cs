using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using static System.Windows.Forms.AxHost;

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
    }
}
