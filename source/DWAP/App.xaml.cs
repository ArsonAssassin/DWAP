using Archipelago.Core;
using Archipelago.Core.GameClients;
using Archipelago.Core.MauiGUI;
using Archipelago.Core.MauiGUI.Models;
using Archipelago.Core.MauiGUI.ViewModels;
using Archipelago.Core.Models;
using Archipelago.Core.Util;
using Archipelago.Core.Util.GPS;
using Archipelago.MultiClient.Net.MessageLog.Messages;
using DWAP.Models;
using Newtonsoft.Json;
using Serilog;
using System.Timers;
using Location = Archipelago.Core.Models.Location;
namespace DWAP
{
    public partial class App : Application
    {
        static MainPageViewModel Context;
        public static ArchipelagoClient Client { get; set; }
        public static List<DigimonWorldItem> APItems { get; set; }
        public static List<DigimonWorldItem> DigimonSouls { get; set; }
        public static List<DigimonItem> DigimonItems { get; set; }
        public static List<DigimonTechniqueData> DigimonTechniques { get; set; }
        public static PositionData CurrentLocation { get; set; }
        public static int StatCap { get; set; }
        public static int ExpMultiplier { get; set; }
        public static bool StatCapEnabled { get; set; }
        public static Randomiser RandomSettings { get; set; }
        private System.Timers.Timer _timer1 { get; set; } = new System.Timers.Timer(1000);
        private static readonly object _lockObject = new object();
        private bool _fastDrimogemon = false;
        private bool _easyMonochromon = false;
        public App()
        {
            InitializeComponent();
            _timer1.Elapsed += TimerTick;
            Context = new MainPageViewModel("0.6.2");
            Context.ConnectClicked += Context_ConnectClicked;
            Context.CommandReceived += (e, a) =>
            {
                Client?.SendMessage(a.Command);
            };
            MainPage = new MainPage(Context);
            Context.ConnectButtonEnabled = true;
            Context.UnstuckClicked += (o, e) =>
            {
                Log.Verbose("Current Position: ");
                Log.Verbose(JsonConvert.SerializeObject(CurrentLocation));
            };
            Context.UnstuckVisible = true;
            Log.Information("Initialising collections...");
            Log.Information("Loading Items");
            APItems = Helpers.GetAPItems();
            Log.Information("Loading Souls");
            DigimonSouls = Helpers.GetDigimonSouls();
            DigimonItems = Helpers.GetConsumables();
            Log.Information("Ready to connect!");

        }
        private void AddDigimonItem(int id)
        {
            var localId = id - 692000;
            var consumable = DigimonItems.First(x => x.Id == localId);
            var inventorySize = (int)Memory.ReadByte(Addresses.InventorySize);
            //Get matching item pile in inventory
            for (int i = 0; i < 10; i++)
            {
                ulong slotAddress = (ulong)(0x0013D474 + i);
                ulong amountAddress = (ulong)(0x0013D492 + i);
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
            ulong itemBankAddress = Addresses.ItemBankBaseAddress + (ulong)localId;
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
        private Tuple<ulong, ulong> GetEmptyInventorySlot()
        {
            var inventorySize = (ulong)Memory.ReadByte(Addresses.InventorySize);
            for (int i = 0; i < 10; i++)
            {
                ulong slotAddress = (ulong)(0x0013D474 + i);
                ulong amountAddress = (ulong)(0x0013D492 + i);
                if (Memory.ReadByte(slotAddress) == 255)
                {
                    return new Tuple<ulong, ulong>(slotAddress, amountAddress);
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
            RandomSettings = new Randomiser(randomOptions);
            Log.Logger.Information("Running Randomisation");
            if (options.ContainsKey("easy_monochromon"))
            {
                _easyMonochromon = Convert.ToInt32(options["easy_monochromon"].ToString()) > 0;
            }
            if (options.ContainsKey("fast_drimogemon"))
            {
                _fastDrimogemon = Convert.ToInt32(options["fast_drimogemon"].ToString()) > 0;
            }
            if (options.ContainsKey("random_starter"))
            {
                var starterOption = Convert.ToInt32(options["random_starter"].ToString());
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
            }
            RandomSettings.Generate();
            if (options.ContainsKey("exp_multiplier"))
            {
                ExpMultiplier = Convert.ToInt32(options["exp_multiplier"].ToString());
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
            //if (options.ContainsKey("random_techniques"))
            //{
            //    _ = Task.Run(async () =>
            //    {
            //        try
            //        {
            //            await WaitForJijimonIntro();
            //            WriteLine("Randomising Technique Data");
            //            DigimonTechniques = RandomSettings.ShuffleAndWriteTechniques(DigimonTechniques);
            //        }
            //        catch (Exception ex)
            //        {
            //            WriteLine(ex.Message);
            //        }
            //    }).ConfigureAwait(false);
            //}
            if (options.ContainsKey("random_starter"))
            {
                Log.Information("Writing new Starters");
                Memory.WriteByte(Addresses.Starter1, RandomSettings.Starter);
                Memory.WriteByte(Addresses.Starter2, RandomSettings.Starter);

                Log.Information("Checking for existing moveset");
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
                            Log.Logger.Error(ex.Message);
                        }
                    }).ConfigureAwait(false);
                }

            }


        }

        public async Task WaitForJijimonIntro()
        {
            Log.Information("Game has not started yet, waiting for intro to finish.");
            bool finished = false;
            while (!finished)
            {
                var currentTime = Memory.ReadLong(0x00134f00);
                if (currentTime > 8)
                {
                    finished = true;
                }
                await Task.Delay(100);
            }
            Log.Information("Detected intro finish.");
            return;
        }
        public bool CheckForMoves()
        {
            bool hasMoves = !(Memory.ReadByte(0x00155800) == 0
                && Memory.ReadByte(0x00155805) == 0
                && Memory.ReadByte(0x00155801) == 0
                && Memory.ReadByte(0x00155804) == 0
                && Memory.ReadByte(0x00155802) == 0
                && Memory.ReadByte(0x00155803) == 0
                && Memory.ReadByte(0x00155806) == 0);
            if (hasMoves)
            {
                Log.Information("Moves detected");
            }
            else Log.Warning("No moves");
            return hasMoves;
        }
        private void WriteStarterMove(byte starter)
        {
            Log.Information("Setting Starter Technique");
            var move = GetStarterMove(starter);

            Memory.WriteBit(move.Address, move.AddressBit, true);

            Memory.WriteByte(Addresses.TechniqueSlot1, 46);
        }
        private List<DigimonTechniqueData> ReadTechniques()
        {
            Log.Information("Reading Technique Data");
            List<DigimonTechniqueData> techniques = new List<DigimonTechniqueData>();
            ulong currentAddress = Addresses.TechniqueStartAddress;
            ulong learningChanceAddress = Addresses.LearningChanceStartAddress;
            for (int i = 0; i < 120; i++)
            {
                DigimonTechniqueData tech = new DigimonTechniqueData();
                tech.Slot = i;
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
                tech = tech.PopulateTechData();
                techniques.Add(tech);
            }
            Log.Information("Techniques Loaded");
            return techniques;
        }
        private DigimonTechniqueData GetStarterMove(byte starter)
        {
            var stage = GetDigimonStage(starter);
            if (stage == DigimonStage.baby || stage == DigimonStage.intraining)
            {
                Log.Information("Teaching Bubble");
                return DigimonTechniques.First(x => x.Name == "Bubble");
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
                Log.Information("Teaching Dynamite Kick");
                return DigimonTechniques.First(x => x.Name == "Dynamite Kick");
            }
            if (starter == 62)
            {
                Log.Information("Teaching Fire Tower");
                //Weregarurumon only knows Fire Tower
                return DigimonTechniques.First(x => x.Name == "Fire Tower");
            }
            if (spitFireStarters.Contains(starter))
            {
                Log.Information("Teaching Spit Fire");
                return DigimonTechniques.First(x => x.Name == "Spit Fire");
            }
            if (sonicJabStarters.Contains(starter))
            {
                Log.Information("Teaching Sonic Jab");
                return DigimonTechniques.First(x => x.Name == "Sonic Jab");
            }
            if (staticElectStarters.Contains(starter))
            {
                Log.Information("Teaching Static Elect");
                return DigimonTechniques.First(x => x.Name == "Static Elect");
            }
            if (metalSprintStarters.Contains(starter))
            {
                Log.Information("Teaching Metal Sprinter");
                return DigimonTechniques.First(x => x.Name == "Metal Sprinter");
            }
            if (horizontalKickStarters.Contains(starter))
            {
                Log.Information("Teaching Horizontal Kick");
                return DigimonTechniques.First(x => x.Name == "Horizontal Kick");
            }
            if (teardropStarters.Contains(starter))
            {
                Log.Information("Teaching Tear Drop");
                return DigimonTechniques.First(x => x.Name == "Tear Drop");
            }
            if (poisonClawStarters.Contains(starter))
            {
                Log.Information("Teaching Poison Claw");
                return DigimonTechniques.First(x => x.Name == "Poison Claw");
            }
            return DigimonTechniques.First(x => x.Name == "Spit Fire");

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
            Memory.Write(0x001384AE, multVal);

            Memory.WriteByte(0x001384AC, 63);
            Memory.Write(0x001384B0, (short)9999);
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
        private void TimerTick(object? sender, ElapsedEventArgs e)
        {
            if (ExpMultiplier > 1)
            {
                SetExpMultiplier(ExpMultiplier);
            }
            CurrentLocation = Helpers.GetCurrentLocation();
            EnsureStatCap();
            EnsureSouls();
            EnsureWorldFlags();
            EnsureProsperity();
        }

        private void EnsureProsperity()
        {
            var prosperity = Helpers.CalculateProsperityPoints(Client.GameState);
            Memory.Write(Addresses.ProsperityPoints, prosperity);
        }

        private void EnsureWorldFlags()
        {
            if (_easyMonochromon && CurrentLocation.MapId == 49)
            {
                Memory.Write(Addresses.MonochromeProfitAddress, 4000);
            }
            if (_fastDrimogemon)
            {
                if (Memory.ReadByte(Addresses.HasBeatenDrimogemon) == 1 && Memory.ReadByte(Addresses.MeramonTunnel_DiggingState) == 11)
                {
                    Memory.WriteByte(Addresses.MeramonTunnel_DrimogemonState, 2);
                    Memory.WriteByte(Addresses.MeramonTunnel_State, 10);
                    Memory.WriteByte(Addresses.MeramonTunnel_DiggingState, 5);
                }
            }
        }

        private async void EnsureSouls()
        {
            var locations = Helpers.GetLocations();
            var souls = Helpers.GetMissingSouls(Client);
            foreach (var soul in souls)
            {
                var digimonName = soul.Name.Split(" ")[0];
                var recruitLocation =(Location) locations.FirstOrDefault(x => x.Name == digimonName);
                
                Memory.WriteBit(recruitLocation.Address, recruitLocation.AddressBit, false);
            }
        }
        public async Task Connect(ConnectClickedEventArgs args)
        {
            if (Client != null)
            {
                Client.Connected -= OnConnected;
                Client.Disconnected -= OnDisconnected;
            }
            DuckstationClient client = new DuckstationClient();
            var duckstationConnected = client.Connect();
            if (!duckstationConnected)
            {
                Log.Warning("Duckstation not running, open Duckstation and launch the game before connecting!");
                return;
            }
            Client = new ArchipelagoClient(client);

            Addresses.DuckstationOffset = Memory.GetDuckstationOffset();
            Memory.GlobalOffset = Addresses.DuckstationOffset;

            Client.Connected += OnConnected;
            Client.Disconnected += OnDisconnected;

            await Client.Connect(args.Host, "Digimon World");

            await Client.Login(args.Slot, !string.IsNullOrWhiteSpace(args.Password) ? args.Password : null);

            DigimonTechniques = ReadTechniques();
            var locations = Helpers.GetProsperityLocations();
            locations.AddRange(Helpers.GetDigimonCards());

            Client.MonitorLocations(locations);
            Client.GPSHandler = new Archipelago.Core.Util.GPS.GPSHandler(() => Helpers.GetCurrentLocation());
            Client.GPSHandler.PositionChanged += (o, e) => 
            {
                Log.Verbose($"Position: {e.NewX} {e.NewY}");
            };
            Client.GPSHandler.MapChanged += (o, e) =>
            {
                Log.Debug($"Map Changed: {Client.GPSHandler.Region}: {e.NewMapName}");
            };
            _timer1.Start();
            if (Client.Options != null)
            {
                ConfigureOptions(Client.Options);
            }
            Client.ItemReceived += (e, args) =>
            {
                Log.Information($"Item Received: {JsonConvert.SerializeObject(args.Item)}");
                if (APItems.Any(x => x.Id == args.Item.Id))
                {
                    var item = APItems.First(x => x.Id == args.Item.Id);
                    if (item.Type == ItemType.Consumable || item.Type == ItemType.DV)
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
                else if(DigimonSouls.Any(x => x.Id == args.Item.Id))
                {
                    var item = DigimonSouls.First(x => x.Id == args.Item.Id);
                    if (item.Type == ItemType.Soul)
                    {
                        var soulName = item.Name.Split(" ")[0];
                        var digimonRecruit = Helpers.GetLocations().Where(x => x.Name.Contains(soulName)).ToList();
                        Client.MonitorLocations(digimonRecruit);
                    }
                }
            };

            if (!Client.GameState.CompletedLocations.Any(x => x.Id == 69003000))
            {
                _ = Task.Run(async () =>
                {
                    try
                    {
                        await WaitForJijimonIntro();
                        var startGameLocation = new Archipelago.Core.Models.Location() { Id = 69003000, Name = "Start Game" };
                        Client.SendLocation(startGameLocation);
                        Client.GameState.CompletedLocations.Add(startGameLocation);
                    }
                    catch (Exception ex)
                    {
                        Log.Logger.Error(ex.Message);
                    }
                }).ConfigureAwait(false);
            }
            var soulLocations = new List<Archipelago.Core.Models.ILocation>();
            var acquiredSouls = Helpers.GetAcquiredSouls(Client);
            if (acquiredSouls.Any())
            {
                var recruitLocations = Helpers.GetLocations();
                foreach (var soul in acquiredSouls)
                {
                    var digimonName = soul.Name.Split(" ")[0];
                    var recruitLocation = recruitLocations.FirstOrDefault(x => x.Name == digimonName);
                    soulLocations.Add(recruitLocation);
                }
                if (soulLocations.Any())
                {
                    Client.MonitorLocations(soulLocations);
                }
            }

            var goalLocation = Helpers.GetLocations().Single(x => x.Name == "Digitamamon");
            if (goalLocation.Check())
            {
                Client.SendGoalCompletion();
            }
        }
        private void Context_ConnectClicked(object? sender, ConnectClickedEventArgs e)
        {
            if (Client == null || !(Client?.IsConnected ?? false))
            {
                Connect(e).ConfigureAwait(false);
            }
            else if (Client != null)
            {
                Log.Information("Disconnecting...");
                Client.Disconnect();
            }
        }
        private static void LogItem(Item item)
        {
            var messageToLog = new LogListItem(new List<TextSpan>()
            {
                new TextSpan(){Text = $"[{item.Id.ToString()}] -", TextColor = Color.FromRgb(255, 255, 255)},
                new TextSpan(){Text = $"{item.Name}", TextColor = Color.FromRgb(200, 255, 200)},
            });
            lock (_lockObject)
            {
                Microsoft.Maui.Controls.Application.Current.Dispatcher.DispatchAsync(() =>
                {
                    Context.ItemList.Add(messageToLog);
                });
            }
        }

        private void Client_MessageReceived(object? sender, Archipelago.Core.Models.MessageReceivedEventArgs e)
        {
            if (e.Message.Parts.Any(x => x.Text == "[Hint]: "))
            {
                LogHint(e.Message);
            }
            Log.Information(JsonConvert.SerializeObject(e.Message));
        }
        private static void LogHint(LogMessage message)
        {
            var newMessage = message.Parts.Select(x => x.Text);

            if (Context.HintList.Any(x => x.TextSpans.Select(y => y.Text) == newMessage))
            {
                return; //Hint already in list
            }
            List<TextSpan> spans = new List<TextSpan>();
            foreach (var part in message.Parts)
            {
                spans.Add(new TextSpan() { Text = part.Text, TextColor = Color.FromRgb(part.Color.R, part.Color.G, part.Color.B) });
            }
            lock (_lockObject)
            {
                Microsoft.Maui.Controls.Application.Current.Dispatcher.DispatchAsync(() =>
                {
                    Context.HintList.Add(new LogListItem(spans));
                });
            }
        }
        private static void OnConnected(object sender, EventArgs args)
        {
            Log.Information("Connected to Archipelago");
            Log.Information($"Playing {Client.CurrentSession.ConnectionInfo.Game} as {Client.CurrentSession.Players.GetPlayerName(Client.CurrentSession.ConnectionInfo.Slot)}");
        }

        private static void OnDisconnected(object sender, EventArgs args)
        {
            Log.Information("Disconnected from Archipelago");
        }
        protected override Microsoft.Maui.Controls.Window CreateWindow(IActivationState activationState)
        {
            var window = base.CreateWindow(activationState);
            if (DeviceInfo.Current.Platform == DevicePlatform.WinUI)
            {
                window.Title = "DWAP - Digimon World Archipelago Randomizer";                
            }
            window.Width = 600;

            return window;
        }
    }
}
