using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

namespace DWAP.RomPatcher
{
    public static class Helpers
    {
        public static string GetFormat<T>(this T input) where T : IDigimonWorldDataStructure
        {
            var formatAttribute = typeof(T).GetCustomAttribute<DigimonWorldDataFormatAttribute>();
            if (formatAttribute == null)
            {
                throw new InvalidOperationException($"The class {typeof(T).Name} must have a DigimonWorldDataFormat attribute.");
            }

            string format = formatAttribute.Format;
            return format;
        }
        public static string GetFormat<T>() where T : IDigimonWorldDataStructure
        {
            // Get the type of T
            var type = typeof(T);

            // Get the DigimonDataFormatAttribute from the type
            var formatAttribute = type.GetCustomAttribute<DigimonWorldDataFormatAttribute>();
            if (formatAttribute == null)
            {
                throw new ArgumentException($"Type {type.Name} does not have a DigimonDataFormat attribute.");
            }

            return formatAttribute.Format;
        }
    }
}
