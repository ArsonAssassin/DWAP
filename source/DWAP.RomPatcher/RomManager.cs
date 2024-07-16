using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Reflection.PortableExecutable;
using System.Text;
using System.Threading.Tasks;

namespace DWAP.RomPatcher
{
    public class RomManager
    {
        public DigimonWorldRomData ReadRom(string filePath)
        {
            var FullData = new DigimonWorldRomData();
            var stream = File.OpenRead(filePath);
            var bigScript = new DigimonWorldTextBox();
            using (BinaryReader reader = new BinaryReader(stream))
            {
                var tokomonItems = ReadTokomonItems(reader);



                //var scriptStartAddress = 0x13FD5809;


                    var vendingAddress = 0x13FE31C8;
                var vending = ReadDataBlock<DigimonWorldTextBox>(reader, vendingAddress, 100);

                
                FullData.JijimonIntroText = ReadJijimonIntro(reader);
                FullData.JijimonIntroText.data = "I'm Jijimon.\rWelcome to Archipelago!\rJijimon \r";
           //     bigScript = ReadDataBlock<DigimonWorldTextBox>(reader, 0x00000000, (int)reader.BaseStream.Length);
            }

            return FullData;
        }
        public void WriteRom(string romPath, DigimonWorldRomData data)
        {
            using (var writer = new BinaryWriter(File.Create(romPath)))
            {

                WriteDataBlock(writer, new TokomonItem() { Cmd = 40, Count = 1, Item = 70 }, 0x14071064);
                WriteDataBlock(writer, new TokomonItem() { Cmd = 40, Count = 3, Item = 67 }, 0x14071068);

                WriteDataBlock(writer, data.JijimonIntroText, 0x140BD212);

            }

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
        private DigimonWorldTextBox ReadJijimonIntro(BinaryReader reader)
        {
            var jijimonText = new DigimonWorldTextBox();
            var jijimonTextAddress = 0x140BD212;
            jijimonText = ReadDataBlock<DigimonWorldTextBox>(reader, jijimonTextAddress, 100);
            return jijimonText;
        }

    }
}

