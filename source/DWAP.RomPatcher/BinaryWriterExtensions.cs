using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

namespace DWAP.RomPatcher
{
    public static class BinaryWriterExtensions
    {
        public static void Write<T>(this BinaryWriter writer, T input, long address) where T : IDigimonWorldDataStructure
        {
            var properties = typeof(T).GetProperties()
           .Where(p => p.GetCustomAttributes(typeof(BinaryFieldAttribute), false).Any())
           .OrderBy(p => ((BinaryFieldAttribute)p.GetCustomAttributes(typeof(BinaryFieldAttribute), false).First()).Order)
           .ToArray();
            

            byte[] dataToWrite = new byte[FormatReader.GetSize(input.GetFormat())];

            for(int i = 0; i < dataToWrite.Length; i++)
            {
                if (properties.Any(x => ((BinaryFieldAttribute)x.GetCustomAttributes(typeof(BinaryFieldAttribute), false).First()).Order == i))
                {
                    var prop = properties.First(x => ((BinaryFieldAttribute)x.GetCustomAttributes(typeof(BinaryFieldAttribute), false).First()).Order == i);
                    var currData = ConvertToByteArray(prop.GetValue(input), prop.PropertyType);
                    Array.Copy(currData, 0, dataToWrite, i, currData.Length);
                    if (currData.Length > 1) i += currData.Length - 1;

                }
            }
            writer.Write(dataToWrite);
        }

        private static byte[] ConvertToByteArray(object value, Type type)
        {
            if (value == null)
            {
                throw new ArgumentNullException(nameof(value));
            }

            if (type.IsEnum)
            {
                type = Enum.GetUnderlyingType(type);
            }

            if (type == typeof(byte))
            {
                return new byte[] { (byte)value };
            }
            if (type == typeof(bool))
            {
                return BitConverter.GetBytes((bool)value);
            }
            if (type == typeof(short))
            {
                return BitConverter.GetBytes((short)value);
            }
            if (type == typeof(int))
            {
                return BitConverter.GetBytes((int)value);
            }
            if (type == typeof(long))
            {
                return BitConverter.GetBytes((long)value);
            }
            if (type == typeof(float))
            {
                return BitConverter.GetBytes((float)value);
            }
            if (type == typeof(double))
            {
                return BitConverter.GetBytes((double)value);
            }
            if (type == typeof(char))
            {
                return BitConverter.GetBytes((char)value);
            }

            throw new ArgumentException($"Unsupported type: {type}");
        }
    }

}
