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
                    if (currData == null) continue;
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
            if(value is byte[] data)
            {
                return data;
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
            if(type == typeof(string))
            {
                return GameStringToBytes((string)value, true);
            }
            throw new ArgumentException($"Unsupported type: {type}");
        }


        public static byte[] GameStringToBytes(string input, bool ignoreAscii)
        {
            using (var stream = new MemoryStream())
            using (var writer = new BinaryWriter(stream))
            {
                foreach (char ch in input)
                {
                    if (ch >= 0x20 && ch <= 0x7F && !ignoreAscii)
                    {
                        writer.Write((byte)ch);
                    }
                    else if (ch == 0x0D) // \r
                    {
                        writer.Write((byte)ch);
                    }
                    else
                    {
                        byte[] bytes = GetGameCharacterBytes(ch);
                        if (bytes != null)
                        {
                            writer.Write(bytes);
                        }
                        else
                        {
                            // Handle unknown characters
                            writer.Write((byte)'Ä'); // Using Ä as a placeholder for unknown characters
                        }
                    }
                }

                return stream.ToArray();
            }
        }
        private static byte[] GetGameCharacterBytes(char character)
        {
            switch (character)
            {
                case '0': return new byte[] { 0x82, 79 };
                case '1': return new byte[] { 0x82, 80 };
                case '2': return new byte[] { 0x82, 81 };
                case '3': return new byte[] { 0x82, 82 };
                case '4': return new byte[] { 0x82, 83 };
                case '5': return new byte[] { 0x82, 84 };
                case '6': return new byte[] { 0x82, 85 };
                case '7': return new byte[] { 0x82, 86 };
                case '8': return new byte[] { 0x82, 87 };
                case '9': return new byte[] { 0x82, 88 };
                case '\\': return new byte[] { 0x82, 95 }; // or 0x129, 95 based on context
                case 'A': return new byte[] { 0x82, 96 };
                case 'B': return new byte[] { 0x82, 97 };
                case 'C': return new byte[] { 0x82, 98 };
                case 'D': return new byte[] { 0x82, 99 };
                case 'E': return new byte[] { 0x82, 100 };
                case 'F': return new byte[] { 0x82, 101 };
                case 'G': return new byte[] { 0x82, 102 };
                case 'H': return new byte[] { 0x82, 103 };
                case 'I': return new byte[] { 0x82, 104 };
                case 'J': return new byte[] { 0x82, 105 };
                case 'K': return new byte[] { 0x82, 106 };
                case 'L': return new byte[] { 0x82, 107 };
                case 'M': return new byte[] { 0x82, 108 };
                case 'N': return new byte[] { 0x82, 109 };
                case 'O': return new byte[] { 0x82, 110 };
                case 'P': return new byte[] { 0x82, 111 };
                case 'Q': return new byte[] { 0x82, 112 };
                case 'R': return new byte[] { 0x82, 113 };
                case 'S': return new byte[] { 0x82, 114 };
                case 'T': return new byte[] { 0x82, 115 };
                case 'U': return new byte[] { 0x82, 116 };
                case 'V': return new byte[] { 0x82, 117 };
                case 'W': return new byte[] { 0x82, 118 };
                case 'X': return new byte[] { 0x82, 119 };
                case 'Y': return new byte[] { 0x82, 120 };
                case 'Z': return new byte[] { 0x82, 121 };
                case 'a': return new byte[] { 0x82, 129 };
                case 'b': return new byte[] { 0x82, 130 };
                case 'c': return new byte[] { 0x82, 131 };
                case 'd': return new byte[] { 0x82, 132 };
                case 'e': return new byte[] { 0x82, 133 };
                case 'f': return new byte[] { 0x82, 134 };
                case 'g': return new byte[] { 0x82, 135 };
                case 'h': return new byte[] { 0x82, 136 };
                case 'i': return new byte[] { 0x82, 137 };
                case 'j': return new byte[] { 0x82, 138 };
                case 'k': return new byte[] { 0x82, 139 };
                case 'l': return new byte[] { 0x82, 140 };
                case 'm': return new byte[] { 0x82, 141 };
                case 'n': return new byte[] { 0x82, 142 };
                case 'o': return new byte[] { 0x82, 143 };
                case 'p': return new byte[] { 0x82, 144 };
                case 'q': return new byte[] { 0x82, 145 };
                case 'r': return new byte[] { 0x82, 146 };
                case 's': return new byte[] { 0x82, 147 };
                case 't': return new byte[] { 0x82, 148 };
                case 'u': return new byte[] { 0x82, 149 };
                case 'v': return new byte[] { 0x82, 150 };
                case 'w': return new byte[] { 0x82, 151 };
                case 'x': return new byte[] { 0x82, 152 };
                case 'y': return new byte[] { 0x82, 153 };
                case 'z': return new byte[] { 0x82, 154 };
                case ' ': return new byte[] { 0x81, 64 };
                case '.': return new byte[] { 0x81, 66 };
                case ',': return new byte[] { 0x81, 67 };
                case ':': return new byte[] { 0x81, 70 };
                case ';': return new byte[] { 0x81, 71 };
                case '?': return new byte[] { 0x81, 72 };
                case '!': return new byte[] { 0x81, 73 };
                case '\'': return new byte[] { 0x81, 117 };
                case '+': return new byte[] { 0x81, 123 };
                case '-': return new byte[] { 0x81, 124 };
                default: return null;
            }
        }


    }

}
