using Archipelago.ePSXe;
using Archipelago.ePSXe.Models;
using Archipelago.ePSXe.Util;
using DWAP.RomPatcher;
using Newtonsoft.Json;
using System.Text;

namespace DWAP
{
    public partial class Form1 : Form
    {
        public static ArchipelagoClient Client { get; set; }
        public static List<DigimonWorldItem> Items { get; set; }
        public static List<Recruitment> RecruitList { get; set; }
        public static List<DigimonItem> DigimonItems { get; set; }
        public static int StatCap { get; set; }
        public static int ExpMultiplier { get; set; }
        public static bool StatCapEnabled { get; set; }
        public Form1()
        {
            InitializeComponent();
            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
#if DEBUG
            button1.Enabled = true;
            button1.Visible = true;
#endif

        }

        public async Task Connect()
        {
            ePSXeClient client = new ePSXeClient();
            var ePSXeConnected = client.Connect();
            if (!ePSXeConnected)
            {
                WriteLine("ePSXE not running, open ePSXe and launch the game before connecting!");
                return;
            }
            Client = new ArchipelagoClient();
            Client.Connected += (e, args) =>
            {
                WriteLine("Connected to Archipelago");
                WriteLine($"Playing {Client.CurrentSession.ConnectionInfo.Game} as {Client.CurrentSession.Players.GetPlayerName(Client.CurrentSession.ConnectionInfo.Slot)}");
                connectBtn.Text = "Disconnect";
            };
            Client.Disconnected += (e, args) =>
            {
                WriteLine("Disconnected from Archipelago");
                connectBtn.Text = "Connect";
            };
            await Client.Connect(hostTextbox.Text, "Digimon World");
            // var locations = Helpers.GetLocations();
            var locations = GetRecruitmentLocations();
            locations.AddRange(Helpers.GetTemp());
            Client.PopulateLocations(locations);
            await Client.Login(slotTextbox.Text, !string.IsNullOrWhiteSpace(passwordTextbox.Text) ? passwordTextbox.Text : null);
           
            timer1.Start();
            ConfigureOptions(Client.Options);

            Client.ItemReceived += (e, args) =>
            {
                WriteLine($"Item Received: {JsonConvert.SerializeObject(args.Item)}");
                if (Items.Any(x => x.Id == args.Item.Id))
                {
                    var item = Items.First(x => x.Id == args.Item.Id);
                    if (item.Type == ItemType.Recruitment)
                    {
                        RecruitDigimon(item.Name);
                        //      EnsureRecruitment();
                    }
                    else if (item.Type == ItemType.Consumable)
                    {
                        AddDigimonItem(item.Id);
                    }
                    else if (item.Name == "1000 Bits")
                    {
                        AddMoney(1000);
                    }
                    else if (item.Name == "5000 Bits")
                    {
                        AddMoney(5000);
                    }
                    else if (item.Name == "Progressive Stat Cap")
                    {
                        var boostsReceived = (Client.CurrentSession.Items.AllItemsReceived.Count(x => x.ItemName.ToLower() == "progressive stat cap"));
                        if (boostsReceived >= 9)
                        {
                            StatCap = 999;
                        }
                        else StatCap = (boostsReceived * 100) + 100;
                    }
                }
            };
        }
        private void AddDigimonItem(int id)
        {
            var localId = id - 692000;
            var consumable = DigimonItems.First(x => x.Id == localId);
            var inventorySize = (int)Memory.ReadByte(Addresses.InventorySize);
            //Get matching item pile in inventory
            for (int i = 0; i < inventorySize; i++)
            {
                var slotAddress = 0x00B94E14 + i;
                var amountAddress = 0x00B94E32 + i;
                var currentItemInSlot = Memory.ReadByte(slotAddress);
                if (currentItemInSlot == consumable.Id)
                {
                    var currentAmount = (int)Memory.ReadByte(amountAddress);
                    Memory.WriteByte(amountAddress, (byte)(currentAmount + 1));
                    return;
                }
            }

            //Item not already in inventory, find empty space
            var invSlot = GetEmptyInventorySlot();
            if(invSlot != null)
            {
                Memory.WriteByte(invSlot.Item1, (byte)localId);
                Memory.WriteByte(invSlot.Item2, 1);
                return;
            }

            //add to item bank
            var itemBankAddress = Addresses.ItemBankBaseAddress + localId;
            var storedItemCount = Memory.ReadByte(itemBankAddress);
            if (storedItemCount == 255)
            {
                Memory.WriteByte(itemBankAddress, 1);
            }
            else
            {
                Memory.WriteByte(itemBankAddress, (byte)(Memory.ReadByte(itemBankAddress) + 1));
            }
        }

        private Tuple<int, int> GetEmptyInventorySlot()
        {
            var inventorySize = (int)Memory.ReadByte(Addresses.InventorySize);
            for (int i = 0; i < inventorySize; i++)
            {
                var slotAddress = 0x00B94E14 + i;
                var amountAddress = 0x00B94E32 + i;
                if (Memory.ReadByte(slotAddress) == 255)
                {
                    return new Tuple<int, int>(slotAddress, amountAddress);
                }
            }
            return null;
        }
        private void AddMoney(int amount)
        {
            var currentCash = Memory.ReadInt(Addresses.CurrentBits);
            var newCash = currentCash + amount;
            Memory.Write(Addresses.CurrentBits, newCash);
        }
        private void ConfigureOptions(Dictionary<string, object> options)
        {
            if (options.ContainsKey("exp_multiplier"))
            {
                ExpMultiplier = Convert.ToInt32(options["exp_multiplier"]);
            }
            if (options.ContainsKey("progressive_stats"))
            {
                StatCapEnabled = true;
                var boostsReceived = (Client.CurrentSession.Items.AllItemsReceived.Count(x => x.ItemName.ToLower() == "progressive stat cap"));
                if (boostsReceived >= 9)
                {
                    StatCap = 999;
                }
                else StatCap = (boostsReceived * 100) + 100;
            }
            if (options.ContainsKey("random_starter"))
            {
                var starterOption = Convert.ToInt32(options["random_starter"]);
                if (starterOption == 0)
                {
                    return;
                }
                WriteLine("Randomising Starter");
                var seed = Client.CurrentSession.RoomState.Seed;
                var numericSeed = 0;
                foreach (char c in seed)
                {
                    numericSeed += Convert.ToInt32(c);
                }
                var random = new Random(numericSeed);
                if (starterOption == 1)
                {
                    var option1 = (byte)random.Next(1, 65);
                    var option2 = (byte)random.Next(1, 65);
                    Memory.WriteByte(Addresses.Starter1, option1);
                    Memory.WriteByte(Addresses.Starter2, option2);
                }
                else if (starterOption == 2)
                {
                    var option1 = (byte)Helpers.GetRookieNum(random.Next(0, 8));
                    var option2 = (byte)Helpers.GetRookieNum(random.Next(0, 8));
                    Memory.WriteByte(Addresses.Starter1, option1);
                    Memory.WriteByte(Addresses.Starter2, option2);
                }
            }
        }

        private void SetExpMultiplier(int multiplier)
        {
            var multVal = multiplier * 10;
            Memory.Write(0x00B8FE4E, multVal);

            Memory.WriteByte(0x00B8FE4C, 63);
            Memory.Write(0x00B8FE50, 9999);
        }
        private List<Location> GetRecruitmentLocations()
        {
            var recruits = Helpers.GetRecruitment();
            var locations = Helpers.GetLocations();

            var result = new List<Location>();
            foreach (var recruit in recruits)
            {
                var location = new Location
                {
                    Id = locations.First(x => x.Name.ToLower() == recruit.Name.ToLower()).Id,
                    Address = recruit.Address,
                    AddressBit = recruit.AddressBit,
                    Name = recruit.Name,
                    CheckType = LocationCheckType.Bit,
                    CompareType = LocationCheckCompareType.Match
                };
                result.Add(location);

            }
            return result;
        }
        private void RecruitDigimon(string name)
        {
            WriteLine($"Recruiting {name}");

            var recruit = RecruitList.First(x => x.Name.ToLower() == name.ToLower());
            recruit.IsRecruited = true;
            Memory.WriteBit(recruit.Address, recruit.AddressBit, true);
        }

        private void EnsureRecruitment()
        {
            foreach (var digimon in RecruitList)
            {
                //   Memory.WriteBit(digimon.Address, digimon.AddressBit, digimon.IsRecruited);
            }
        }
        private void EnsureStatCap()
        {
            var boostsReceived = (Client.CurrentSession.Items.AllItemsReceived.Count(x => x.ItemName.ToLower() == "progressive stat cap"));
            if (boostsReceived >= 9)
            {
                StatCap = 999;
            }
            else StatCap = (boostsReceived * 100) + 100;
            var currHpMax = Memory.ReadShort(Addresses.MaxHp);
            var currMpMax = Memory.ReadShort(Addresses.MaxMp);
            var currOff = Memory.ReadShort(Addresses.CurrentOffense);
            var currDef = Memory.ReadShort(Addresses.CurrentDefence);
            var currSpd = Memory.ReadShort(Addresses.CurrentSpeed);
            var currBrn = Memory.ReadShort(Addresses.CurrentBrains);

            if (StatCap < 999)
            {
                Memory.Write(Addresses.MaxHp, (short)Math.Min(currHpMax, (short)(StatCap * 10)));
                Memory.Write(Addresses.MaxMp, (short)Math.Min(currMpMax, (short)(StatCap * 10)));
            }
            else
            {
                Memory.Write(Addresses.MaxHp, (short)Math.Min(currHpMax, (short)9999));
                Memory.Write(Addresses.MaxMp, (short)Math.Min(currMpMax, (short)9999));
            }
            Memory.Write(Addresses.CurrentOffense, (short)Math.Min(currOff, StatCap));
            Memory.Write(Addresses.CurrentDefence, (short)Math.Min(currDef, StatCap));
            Memory.Write(Addresses.CurrentSpeed, (short)Math.Min(currSpd, StatCap));
            Memory.Write(Addresses.CurrentBrains, (short)Math.Min(currBrn, StatCap));
        }
        public void WriteLine(string output)
        {
            Invoke(() =>
            {
                outputTextbox.Text += output;
                outputTextbox.Text += System.Environment.NewLine;
            });
        }

        private async void connectbtn_Click(object sender, EventArgs e)
        {
            var valid = ValidateSettings();
            if (!valid)
            {
                WriteLine("Invalid settings, please check your input and try again.");
                return;
            }
            Connect().ConfigureAwait(false);
        }
        private bool ValidateSettings()
        {
            var valid = !string.IsNullOrWhiteSpace(hostTextbox.Text) && !string.IsNullOrWhiteSpace(slotTextbox.Text);
            return valid;
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            if (ExpMultiplier > 1)
            {
                SetExpMultiplier(ExpMultiplier);
            }
            EnsureStatCap();
            //EnsureRecruitment();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

            WriteLine("DWAP - Digimon world Archipelago Randomiser");
            WriteLine("-- By ArsonAssassin --");
            WriteLine("Initialising collections...");
            Items = Helpers.GetItems();
            RecruitList = Helpers.GetRecruitment();
            DigimonItems = Helpers.GetConsumables();
            WriteLine("Ready to connect!");
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Invoke(() =>
            {

                var dlg = new OpenFileDialog();
                dlg.Filter = "Disc Image Files|*.bin";
                var result = dlg.ShowDialog();
                if (result == DialogResult.OK)
                {
                    var file = dlg.FileName;
                    RomManager mgr = new RomManager();
                    var output = mgr.ReadRom(file);

                    mgr.WriteRom(Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.Desktop), "digimonWorldClone.bin"), output);
                    WriteLine("Finished patching ROM");
                }
            });
        }
    }
}
