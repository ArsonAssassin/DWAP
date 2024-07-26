using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DWAP
{
    public class RandomiserOptions
    {
        public int Seed { get; set; }
        public StarterRandomisation StarterRandomisation { get; set; }
        public RandomiserOptions(int seed)
        {
            Seed = seed;
        }
    }
}
