using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DWAP.RomPatcher
{
    public static class FormatReader
    {
        public static int GetSize(string format)
        {
            int size = 0;
            for (int i = 0; i < format.Length; i++)
            {
                var currentChar = format[i];
                if (Char.IsDigit(currentChar))
                {
                    for (int j = 0; j < Convert.ToInt32(currentChar); j++)
                    {
                       var charSize = GetCharSize(format[i + 1]);
                        size += charSize;
                    }
                }
                else
                {
                    size += GetCharSize(format[i]);
                }
            }
            return size;
        }
        private static int GetCharSize(char c)
        {
            switch (c)
            {
                case 'b':
                case 'B':
                case 'c':
                case '?':
                case 'x':
                    return 1;
                case 'h':
                case 'H':
                    return 2;
                case 'i':
                case 'I':
                case 'f':
                case 'l':
                case 'L':
                    return 4;
                case 'd':
                case 'q':
                case 'Q':
                    return 8;
                default:
                    return 0;
            }
        }
    }
}
