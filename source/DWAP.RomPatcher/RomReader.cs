using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Reflection.PortableExecutable;
using System.Text;
using System.Threading.Tasks;

namespace DWAP.RomPatcher
{
    public class RomReader
    {
        public object ReadRom(string filePath)
        {
            //var stream = File.OpenRead(filePath);
            //using (BinaryReader reader = new BinaryReader(stream))
            //{
            //    var tokomonItems = ReadTokomonItems(reader);


            //    return tokomonItems;
            //}


            var stream = File.OpenWrite(filePath);
            using (BinaryWriter writer = new BinaryWriter(stream))
            {
                WriteDataBlock(writer, new TokomonItem() {Cmd = 40, Count = 1, Item = 70}, 0x14071064);
            }


            return null;
        }

        private T ReadDataBlock<T>(BinaryReader reader, long blockStartAddress, int blockSize) where T : IDigimonWorldDataStructure
        {
            reader.BaseStream.Seek(blockStartAddress, SeekOrigin.Begin);
            T item = reader.Read<T>(blockSize);

            return item;
        }

        private void WriteDataBlock<T>(BinaryWriter writer, T obj, long startAddress) where T : IDigimonWorldDataStructure
        {
            writer.BaseStream.Seek(startAddress, SeekOrigin.Begin);
            writer.Write(obj, startAddress);

        }
        private List<TokomonItem> ReadTokomonItems(BinaryReader reader)
        {
            var tokomonItems = new List<TokomonItem>();

            var tokomonItemAddress = 0x14071064;
            var tokomonItemCount = 6;

            for(int i = 0; i < tokomonItemCount; i++)
            {                
                var toko = ReadDataBlock<TokomonItem>(reader, tokomonItemAddress + (i * FormatReader.GetSize(Helpers.GetFormat<TokomonItem>())), FormatReader.GetSize(Helpers.GetFormat<TokomonItem>()));
                tokomonItems.Add(toko);
            }
            return tokomonItems;
        }
    }
}

