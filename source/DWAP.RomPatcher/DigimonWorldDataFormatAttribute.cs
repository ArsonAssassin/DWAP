using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DWAP.RomPatcher
{
    [AttributeUsage(AttributeTargets.Class, Inherited = false)]
    public class DigimonWorldDataFormatAttribute : Attribute
    {
        public string Format { get; }
        public DigimonWorldDataFormatAttribute(string format)
        {
            Format = format;   
        }
    }
}
