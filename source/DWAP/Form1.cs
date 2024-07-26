using Archipelago.ePSXe;
using Archipelago.ePSXe.Models;
using Archipelago.ePSXe.Util;
using DWAP.RomPatcher;
using Newtonsoft.Json;
using System.Media;
using System.Reflection;
using System.Text;
using System.Windows.Forms;
using static System.Windows.Forms.AxHost;
using static System.Windows.Forms.Design.AxImporter;

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
        public static Randomiser RandomSettings { get; set; }
        bool firstConnect = true;
        public Form1()
        {
            InitializeComponent();
            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
            ThreadPool.SetMinThreads(500, 500);
#if DEBUG
            button1.Enabled = true;
            button1.Visible = true;
#endif

        }

        public async Task Connect()
        {
            if (Client != null)
            {
                Client.Connected -= OnConnected;
                Client.Disconnected -= OnDisconnected;
            }
            ePSXeClient client = new ePSXeClient();
            var ePSXeConnected = client.Connect();
            if (!ePSXeConnected)
            {
                WriteLine("ePSXE not running, open ePSXe and launch the game before connecting!");
                return;
            }
            Client = new ArchipelagoClient();


            Client.Connected += OnConnected;
            Client.Disconnected += OnDisconnected;

            await Client.Connect(hostTextbox.Text, "Digimon World");
            // var locations = Helpers.GetLocations();
            var locations = GetRecruitmentLocations();
            locations.AddRange(Helpers.GetTemp());
            Client.PopulateLocations(locations);
            await Client.Login(slotTextbox.Text, !string.IsNullOrWhiteSpace(passwordTextbox.Text) ? passwordTextbox.Text : null);

            timer1.Start();
            ReadTechniques();
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
        private void OnConnected(object sender, EventArgs args)
        {
            WriteLine("Connected to Archipelago");
            WriteLine($"Playing {Client.CurrentSession.ConnectionInfo.Game} as {Client.CurrentSession.Players.GetPlayerName(Client.CurrentSession.ConnectionInfo.Slot)}");
            Invoke(() =>
            {
                connectBtn.Text = "Disconnect";
            });

        }

        private void OnDisconnected(object sender, EventArgs args)
        {
            WriteLine("Disconnected from Archipelago");
            Invoke(() =>
            {
                connectBtn.Text = "Connect";
            });
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
            if (invSlot != null)
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
        private async void ConfigureOptions(Dictionary<string, object> options)
        {
            int randomSeed = 0;
            foreach (char c in Client.CurrentSession.RoomState.Seed)
            {
                randomSeed += Convert.ToInt32(c);
            }
            randomSeed += Client.CurrentSession.ConnectionInfo.Slot;
            var randomOptions = new RandomiserOptions(randomSeed);

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
                    randomOptions.StarterRandomisation = StarterRandomisation.Vanilla;
                }           
                else if (starterOption == 1)
                {
                    randomOptions.StarterRandomisation = StarterRandomisation.All;
                }
                else if (starterOption == 2)
                {
                    randomOptions.StarterRandomisation = StarterRandomisation.RookieOnly;
                   
                }


                RandomSettings = new Randomiser(randomOptions);
                WriteLine("Running Randomisation");
                RandomSettings.Generate();
                WriteLine("Writing new Starters");
                Memory.WriteByte(Addresses.Starter1, RandomSettings.Starter);
                Memory.WriteByte(Addresses.Starter2, RandomSettings.Starter);

                WriteLine("Checking for existing moveset");
                if (!CheckForMoves())
                {
                    _ = Task.Run(async () =>
                    {
                        try
                        {
                            await WaitForJijimonIntro();
                            WriteStarterMove(RandomSettings.Starter);
                        }
                        catch (Exception ex)
                        {
                            WriteLine(ex.Message);
                        }
                    }).ConfigureAwait(false);
                }
            }
        }

        public async Task WaitForJijimonIntro()
        {
            bool finished = false;
            while (!finished)
            {
                var currentTime = Memory.ReadByte(0x00B8C85C) + Memory.ReadByte(0x00B8C85E) + Memory.ReadByte(0x00B8C8A2) + Memory.ReadByte(0x00B8C8A3);
                if (currentTime > 8)
                {
                    finished = true;
                }
                await Task.Delay(100);
            }
            return;
        }
        public bool CheckForMoves()
        {
            bool hasMoves = !(Memory.ReadByte(0x00BAD1A0) == 0
                && Memory.ReadByte(0x00BAD1A5) == 0
                && Memory.ReadByte(0x00BAD1A1) == 0
                && Memory.ReadByte(0x00BAD1A4) == 0
                && Memory.ReadByte(0x00BAD1A2) == 0
                && Memory.ReadByte(0x00BAD1A3) == 0
                && Memory.ReadByte(0x00BAD1A6) == 0);
            if (hasMoves)
            {
                WriteLine("Moves detected");
            }
            else WriteLine("No moves");
            return hasMoves;
        }
        private void WriteStarterMove(byte starter)
        {
            WriteLine("Setting Starter Technique");
            var move = GetStarterMove(starter);
            switch (move)
            {

                case 113:
                case 117:
                    // do nothing for bubbles
                    break;
                case 44:
                    //Dynamite Kick
                    Memory.WriteBit(0x00BAD1A5, 4, true);
                    break;
                case 0:
                    //Fire Tower
                    Memory.WriteBit(0x00BAD1A0, 0, true);
                    break;
                case 2:
                    //Spit Fire
                    Memory.WriteBit(0x00BAD1A0, 2, true);
                    break;
                case 43:
                    //Sonic Jab
                    Memory.WriteBit(0x00BAD1A5, 3, true);
                    break;
                case 12:
                    //Static Elect
                    Memory.WriteBit(0x00BAD1A1, 4, true);
                    break;
                case 26:
                    //Metal Sprinter
                    Memory.WriteBit(0x00BAD1A3, 2, true);
                    break;
                case 55:
                    //Horizontal Kick
                    Memory.WriteBit(0x00BAD1A6, 7, true);
                    break;
                case 23:
                    //Tear drop
                    Memory.WriteBit(0x00BAD1A2, 7, true);
                    break;
                case 37:
                    //Poison Claw
                    Memory.WriteBit(0x00BAD1A4, 5, true);
                    break;
            }
            Memory.WriteByte(Addresses.TechniqueSlot1, 46);
        }
        private void ReadTechniques()
        {
            WriteLine("Reading Technique Data");
            List<DigimonTechniqueData> techniques = new List<DigimonTechniqueData>();
            var currentAddress = Addresses.TechniqueStartAddress;
            var learningChanceAddress = Addresses.LearningChanceStartAddress;
            for(int i = 0; i < 120; i++)
            {
                DigimonTechniqueData tech = new DigimonTechniqueData();
                tech.Unknown1 = Memory.ReadByte(currentAddress);
                currentAddress += Addresses.ByteOffset;
                tech.Unknown2 = Memory.ReadByte(currentAddress);
                currentAddress += Addresses.ByteOffset;
                tech.AITargetDistance = Memory.ReadShort(currentAddress);
                currentAddress += Addresses.ShortOffset;
                tech.Power = Memory.ReadShort(currentAddress);
                currentAddress += Addresses.ShortOffset;
                tech.MP = Memory.ReadByte(currentAddress);
                currentAddress += Addresses.ByteOffset;
                tech.IFrames = Memory.ReadByte(currentAddress);
                currentAddress += Addresses.ByteOffset;
                tech.Range = Memory.ReadByte(currentAddress);
                currentAddress += Addresses.ByteOffset;
                tech.Type = Memory.ReadByte(currentAddress);
                currentAddress += Addresses.ByteOffset;
                tech.StatusEffect = Memory.ReadByte(currentAddress);
                currentAddress += Addresses.ByteOffset;
                tech.BlockingFactor = Memory.ReadByte(currentAddress);
                currentAddress += Addresses.ByteOffset;
                tech.StatusChance = Memory.ReadByte(currentAddress);
                currentAddress += Addresses.ByteOffset;
                tech.Unknown3 = Memory.ReadByte(currentAddress);
                currentAddress += Addresses.ByteOffset;
                tech.Unknown4 = Memory.ReadByte(currentAddress);
                currentAddress += Addresses.ByteOffset;
                tech.Unknown5 = Memory.ReadByte(currentAddress);
                currentAddress += Addresses.ByteOffset;
                tech.LearningChance1 = Memory.ReadByte(learningChanceAddress);
                learningChanceAddress += Addresses.ByteOffset;
                tech.LearningChance2 = Memory.ReadByte(learningChanceAddress);
                learningChanceAddress += Addresses.ByteOffset;
                tech.LearningChance3 = Memory.ReadByte(learningChanceAddress);
                learningChanceAddress += Addresses.ByteOffset;
                techniques.Add(tech);
            }
            WriteLine("Techniques Loaded");
        }
        private byte GetStarterMove(byte starter)
        {
            var stage = GetDigimonStage(starter);
            if (stage == DigimonStage.baby)
            {
                WriteLine("Teaching Bubble");
                return 113;
            }
            if (stage == DigimonStage.intraining)
            {
                WriteLine("Teaching Bubble");
                return 117;
            }

            byte[] spitFireStarters = [3, 5, 7, 8, 9, 10, 19, 21, 22, 34, 36, 45, 47, 56];
            byte[] sonicJabStarters = [6, 13, 14, 17, 23, 26, 27, 31, 38, 42, 48, 51, 58, 63, 65];
            byte[] staticElectStarters = [4, 18, 20, 32, 33, 37, 40, 50, 59];
            byte[] metalSprintStarters = [12, 28, 41, 54, 64];
            byte[] horizontalKickStarters = [11, 39, 53];
            byte[] teardropStarters = [24, 35, 49, 61];
            byte[] poisonClawStarters = [25, 46, 55, 57, 60];
            if (starter == 52)
            {
                //Mojyamon gets Dynamite Kick
                WriteLine("Teaching Dynamite Kick");
                return 0x2C;
            }
            if (starter == 62)
            {
                WriteLine("Teaching Fire Tower");
                //Weregarurumon only knows Fire Tower
                return 0x00;
            }
            if (spitFireStarters.Contains(starter))
            {
                WriteLine("Teaching Spit Fire");
                return 0x02;
            }
            if (sonicJabStarters.Contains(starter))
            {
                WriteLine("Teaching Sonic Jab");
                return 0x2B;
            }
            if (staticElectStarters.Contains(starter))
            {
                WriteLine("Teaching Static Elect");
                return 0x0C;
            }
            if (metalSprintStarters.Contains(starter))
            {
                WriteLine("Teaching Metal Sprinter");
                return 0x1A;
            }
            if (horizontalKickStarters.Contains(starter))
            {
                WriteLine("Teaching Horizontal Kick");
                return 0x37;
            }
            if (teardropStarters.Contains(starter))
            {
                WriteLine("Teaching Tear Drop");
                return 0x17;
            }
            if (poisonClawStarters.Contains(starter))
            {
                WriteLine("Teaching Poison Claw");
                return 0x25;
            }
            return 0x02;

        }
        private DigimonStage GetDigimonStage(byte id)
        {
            byte[] babyIds = [1, 15, 29, 43];
            byte[] inTrainingIds = [2, 16, 30, 44];
            byte[] rookieIds = [3, 4, 17, 18, 31, 32, 45, 46, 57];
            byte[] championIds = [5, 6, 7, 8, 9, 10, 11, 19, 20, 21, 22, 23, 24, 25, 33, 34, 35, 36, 37, 38, 39, 47, 48, 49, 50, 51, 52, 53, 58, 63];
            byte[] ultimateIds = [12, 13, 14, 26, 27, 28, 40, 41, 42, 54, 55, 56, 59, 60, 61, 62, 64, 65];

            if (babyIds.Contains(id)) { return DigimonStage.baby; };
            if (inTrainingIds.Contains(id)) { return DigimonStage.intraining; };
            if (rookieIds.Contains(id)) { return DigimonStage.rookie; };
            if (championIds.Contains(id)) { return DigimonStage.champion; };
            if (ultimateIds.Contains(id)) { return DigimonStage.ultimate; };
            return DigimonStage.baby;
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

                System.Diagnostics.Debug.WriteLine(output + System.Environment.NewLine);
            });
        }

        private async void connectbtn_Click(object sender, EventArgs e)
        {
            if (!(Client?.IsConnected ?? false))
            {
                var valid = ValidateSettings();
                if (!valid)
                {
                    WriteLine("Invalid settings, please check your input and try again.");
                    return;
                }
                Connect().ConfigureAwait(false);
            }
            else
            {
                WriteLine("Disconnecting...");
                Client.Disconnect();
            }
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
            using (Stream imgStream = Assembly.GetExecutingAssembly().GetManifestResourceStream("DWAP.Resources.DWAP.png"))
            {
                var image = new Bitmap(imgStream);
                pictureBox1.Image = image;
            }

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

        private void pictureBox1_Click(object sender, EventArgs e)
        {
            Point clickPosition = pictureBox1.PointToClient(Cursor.Position);
            float relativeX = (float)clickPosition.X / pictureBox1.Width;
            float relativeY = (float)clickPosition.Y / pictureBox1.Height;
            Rectangle agumonRegion = new Rectangle(5, 10, 50, 40); 
            Rectangle elecmonRegion = new Rectangle(55, 0, 40, 50);  
            Rectangle betamonRegion = new Rectangle(75, 20, 50, 40); 
            Rectangle gabumonRegion = new Rectangle(5, 50, 50, 50);  
            Rectangle patamonRegion = new Rectangle(40, 80, 50, 50);  
            Rectangle biyomonRegion = new Rectangle(70, 55, 50, 50); 

            string soundFile = "";

            if (agumonRegion.Contains(clickPosition))
                soundFile = "DWAP.Resources.agumon.wav";
            else if (elecmonRegion.Contains(clickPosition))
                soundFile = "DWAP.Resources.elecmon.wav";
            else if (betamonRegion.Contains(clickPosition))
                soundFile = "DWAP.Resources.betamon.wav";
            else if (gabumonRegion.Contains(clickPosition))
                soundFile = "DWAP.Resources.gabumon.wav";
            else if (patamonRegion.Contains(clickPosition))
                soundFile = "DWAP.Resources.patamon.wav";
            else if (biyomonRegion.Contains(clickPosition))
                soundFile = "DWAP.Resources.biyomon.wav";
            if (!string.IsNullOrWhiteSpace(soundFile))
            {
                using (var stream = Assembly.GetExecutingAssembly().GetManifestResourceStream(soundFile))
                {
                    using (SoundPlayer player = new SoundPlayer(stream))
                    {
                        player.Play();
                    }
                }
            }
        }
    }
}
