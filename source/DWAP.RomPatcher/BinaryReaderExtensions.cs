using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DWAP.RomPatcher
{
    public static class BinaryReaderExtensions
    {
        public static T Read<T>(this BinaryReader reader, int length) where T : IDigimonWorldDataStructure
        {
            var obj = Activator.CreateInstance<T>();
            var properties = typeof(T).GetProperties()
                .Where(p => p.GetCustomAttributes(typeof(BinaryFieldAttribute), false).Any())
                .OrderBy(p => ((BinaryFieldAttribute)p.GetCustomAttributes(typeof(BinaryFieldAttribute), false).First()).Order)
                .ToArray();
            var bytes = reader.ReadBytes(length);

            for (int i = 0; i < properties.Length; i++)
            {
                var property = properties[i];
                var attribute = (BinaryFieldAttribute)property.GetCustomAttributes(typeof(BinaryFieldAttribute), false).First();
                var value = Convert.ChangeType(bytes[attribute.Order], property.PropertyType);
                property.SetValue(obj, value);
            }
            return obj;
        }
    }
}
