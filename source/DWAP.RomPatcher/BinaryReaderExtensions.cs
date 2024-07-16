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
                if (property.Name == "RawData")
                {
                    property.SetValue(obj, bytes);
                }
                else
                {
                    if (property.PropertyType == typeof(string))
                    {

                        var output = ParseGameString(bytes, false);

                        property.SetValue(obj, output);
                    }
                    else
                    {
                        var value = Convert.ChangeType(bytes[attribute.Order], property.PropertyType);
                        property.SetValue(obj, value);
                    }
                }
            }
            return obj;
        }
        public static string ParseGameString(byte[] input, bool ignoreAscii)
        {
            using (var buffer = new MemoryStream(input))
            using (var reader = new BinaryReader(buffer))
            {
                StringBuilder builder = new StringBuilder();

                while (reader.BaseStream.Position < reader.BaseStream.Length)
                {
                    byte value = reader.ReadByte();

                    if ((value == 0x81 || value == 0x82) && reader.BaseStream.Position < reader.BaseStream.Length)
                    {
                        builder.Append(GetGameCharacter(value, reader.ReadByte()));
                    }
                    else if (value >= 0x20 && value <= 0x7F && !ignoreAscii)
                    {
                        builder.Append((char)value);
                    }
                    else if (value == 0x0D)
                    {
                        builder.Append((char)value);
                    }
                }

                return builder.ToString();
            }
        }
        public static string GetGameCharacter(byte value, byte character)
        {
            switch (value)
            {
                case 130: // -126 in signed byte
                    switch (character)
                    {
                        case 79:
                            return "0";
                        case 80:
                            return "1";
                        case 81:
                            return "2";
                        case 82:
                            return "3";
                        case 83:
                            return "4";
                        case 84:
                            return "5";
                        case 85:
                            return "6";
                        case 86:
                            return "7";
                        case 87:
                            return "8";
                        case 88:
                            return "9";
                        case 95: // TODO seems like a bug for me?
                            return "\\";
                        case 96:
                            return "A";
                        case 97:
                            return "B";
                        case 98:
                            return "C";
                        case 99:
                            return "D";
                        case 100:
                            return "E";
                        case 101:
                            return "F";
                        case 102:
                            return "G";
                        case 103:
                            return "H";
                        case 104:
                            return "I";
                        case 105:
                            return "J";
                        case 106:
                            return "K";
                        case 107:
                            return "L";
                        case 108:
                            return "M";
                        case 109:
                            return "N";
                        case 110:
                            return "O";
                        case 111:
                            return "P";
                        case 112:
                            return "Q";
                        case 113:
                            return "R";
                        case 114:
                            return "S";
                        case 115:
                            return "T";
                        case 116:
                            return "U";
                        case 117:
                            return "V";
                        case 118:
                            return "W";
                        case 119:
                            return "X";
                        case 120:
                            return "Y";
                        case 121:
                            return "Z";
                        case 129: // -127 in signed byte
                            return "a";
                        case 130: // -126 in signed byte
                            return "b";
                        case 131: // -125 in signed byte
                            return "c";
                        case 132: // -124 in signed byte
                            return "d";
                        case 133: // -123 in signed byte
                            return "e";
                        case 134: // -122 in signed byte
                            return "f";
                        case 135: // -121 in signed byte
                            return "g";
                        case 136: // -120 in signed byte
                            return "h";
                        case 137: // -119 in signed byte
                            return "i";
                        case 138: // -118 in signed byte
                            return "j";
                        case 139: // -117 in signed byte
                            return "k";
                        case 140: // -116 in signed byte
                            return "l";
                        case 141: // -115 in signed byte
                            return "m";
                        case 142: // -114 in signed byte
                            return "n";
                        case 143: // -113 in signed byte
                            return "o";
                        case 144: // -112 in signed byte
                            return "p";
                        case 145: // -111 in signed byte
                            return "q";
                        case 146: // -110 in signed byte
                            return "r";
                        case 147: // -109 in signed byte
                            return "s";
                        case 148: // -108 in signed byte
                            return "t";
                        case 149: // -107 in signed byte
                            return "u";
                        case 150: // -106 in signed byte
                            return "v";
                        case 151: // -105 in signed byte
                            return "w";
                        case 152: // -104 in signed byte
                            return "x";
                        case 153: // -103 in signed byte
                            return "y";
                        case 154: // -102 in signed byte
                            return "z";
                    }
                    break;
                case 129: // -127 in signed byte
                    switch (character)
                    {
                        case 64:
                            return " ";
                        case 66:
                            return ".";
                        case 67:
                            return ",";
                        case 70:
                            return ":";
                        case 71:
                            return ";";
                        case 72:
                            return "?";
                        case 73:
                            return "!";
                        case 95:
                            return "\\";
                        case 117:
                            return "'";
                        case 123:
                            return "+";
                        case 124:
                            return "-";
                    }
                    break;
            }

            return "Ä";
        }
    }
}
