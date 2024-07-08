using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DWAP.RomPatcher
{
    [AttributeUsage(AttributeTargets.Property)]
    public class BinaryFieldAttribute : Attribute
    {
        public int Order { get; }
        public BinaryFieldAttribute(int order) => Order = order;
    }
}
