using Archipelago.Core;
using Archipelago.Core.AvaloniaGUI.Models;
using Archipelago.Core.AvaloniaGUI.ViewModels;
using Archipelago.Core.AvaloniaGUI.Views;
using Archipelago.Core.Helpers;
using Archipelago.Core.Models;
using Archipelago.Core.Util;
using Archipelago.Core.Util.GPS;
using Archipelago.Core.Util.PlatformMemory;
using Archipelago.MultiClient.Net.MessageLog.Messages;
using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Markup.Xaml;
using Avalonia.Media;
using DWAP.Models;
using Newtonsoft.Json;
using ReactiveUI;
using Serilog;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Concurrency;
using System.Reflection;
using System.Threading.Tasks;
using System.Timers;


namespace DWAP;

public partial class App : Application
{
    internal MainWindow MainWindow;
    static MainWindowViewModel Context;
    public static ArchipelagoClient Client { get; set; }
    public static PositionData CurrentLocation { get; set; }
    public static int StatCap { get; set; }
    public static int ExpMultiplier { get; set; }
    public static bool StatCapEnabled { get; set; }
    public static Randomiser RandomSettings { get; set; }
    private System.Timers.Timer _timer1 { get; set; } = new System.Timers.Timer(TimeSpan.FromSeconds(5));
    private static readonly object _lockObject = new object();
    private bool _fastDrimogemon = false;
    private bool _easyMonochromon = false;
    private ILocation goalLocation;
    public override void Initialize()
    {
        AvaloniaXamlLoader.Load(this);
    }

    public override void OnFrameworkInitializationCompleted()
    {
        Start();
        MainWindow = new MainWindow()
        {
            DataContext = Context
        };
        if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        {
            desktop.MainWindow = MainWindow;
        }
        else if (ApplicationLifetime is ISingleViewApplicationLifetime singleViewPlatform)
        {
            singleViewPlatform.MainView = MainWindow;
        }

        base.OnFrameworkInitializationCompleted();
    }
    private void Start()
    {
        Context = new MainWindowViewModel("0.6.4");
        Context.ClientVersion = Assembly.GetEntryAssembly().GetName().Version.ToString();
        _timer1.Elapsed += TimerTick;
        Context.ConnectClicked += Context_ConnectClicked;
        Context.CommandReceived += (e, a) =>
        {
            Client?.SendMessage(a.Command);
        };

        Context.ConnectButtonEnabled = true;
        Context.UnstuckClicked += (o, e) =>
        {
        };
        Context.UnstuckButtonEnabled = true;
        Log.Information("Initialising collections...");
        Log.Information("Loading Items");
        Helpers.APItems = Helpers.GetAPItems();
        Log.Information("Loading Recruits");
        Helpers.DigimonItems = Helpers.GetConsumables();
        Log.Information("Ready to connect!");
    }
    private void AddDigimonItem(int id)
    {
        var localId = id - 692000;
        var consumable = Helpers.DigimonItems.First(x => x.Id == localId);
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
        if (options.ContainsKey("progressive_stats") && Convert.ToInt32(options["progressive_stats"].ToString()) > 0)
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
        if (options.ContainsKey("random_starter") && Convert.ToInt32(options["random_starter"].ToString()) > 0)
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
                        await Helpers.WaitForJijimonIntroAsync();
                        WriteStarterMove(RandomSettings.Starter);
                    }
                    catch (Exception ex)
                    {
                        Log.Logger.Error(ex.Message);
                    }
                }).ConfigureAwait(false);
            }

        }
        if (options.ContainsKey("goal"))
        {
            var goalSetting = Convert.ToInt32(options["goal"].ToString());
            if (goalSetting == 0)
            {
                if (options.ContainsKey("required_prosperity"))
                {
                    var prosperityRequired = Convert.ToInt32(options["required_prosperity"].ToString());
                    goalLocation = Helpers.GetProsperityLocations().Single(x => x.Name == $"{prosperityRequired} Prosperity");
                }
                else goalLocation = Helpers.GetProsperityLocations().Single(x => x.Name == "100 Prosperity");
            }
            else if (goalSetting == 1)
            {
                goalLocation = Helpers.GetLocations().Single(x => x.Name == "Digitamamon");        
            }
        }
        else
        {
            if (options.ContainsKey("required_prosperity"))
            {
                var prosperityRequired = Convert.ToInt32(options["required_prosperity"].ToString());
                goalLocation = Helpers.GetProsperityLocations().Single(x => x.Name == $"{prosperityRequired} Prosperity");
            }
            else goalLocation = Helpers.GetProsperityLocations().Single(x => x.Name == "100 Prosperity");
        }

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
        var move = Helpers.GetStarterMove(starter);

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


    private void SetExpMultiplier(int multiplier)
    {
        var multVal = multiplier * 10;
        Memory.Write(0x001384AE, multVal);

        Memory.WriteByte(0x001384AC, 63);
        Memory.Write(0x001384B0, (short)9999);
    }

    private void EnsureStatCap()
    {
        if (!StatCapEnabled) { return; }
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
        EnsureRecruits();
        EnsureWorldFlags();
        EnsureProsperity();

        if (goalLocation?.Check() ?? false)
        {
            Client.SendGoalCompletion();
        }
    }

    private void EnsureProsperity()
    {
        var prosperity = Helpers.CalculateProsperityPoints();
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
            var hasBeatenDrimogemon = Memory.ReadByte(Addresses.HasBeatenDrimogemon);
            var meramonDigState = Memory.ReadByte(Addresses.MeramonTunnel_DiggingState);
            var meramonTunnelState = Memory.ReadByte(Addresses.MeramonTunnel_State);
            if (hasBeatenDrimogemon == 1 && ( meramonDigState != 5 && meramonTunnelState != 10))
            {
                Memory.WriteByte(Addresses.MeramonTunnel_DrimogemonState, 2); // set Drimogemon to already talked to
                Memory.WriteByte(Addresses.MeramonTunnel_State, 10);          // set tunnel as already dug
                Memory.WriteByte(Addresses.MeramonTunnel_DiggingState, 5);    // set pile as empty
            }
        }
    }

    private async void EnsureRecruits()
    {
        var locations = Helpers.GetLocations();

        // Set town-presence flags (old range) for received recruits
        var acquiredRecruits = Helpers.GetAcquiredRecruits(Client);
        foreach (var recruit in acquiredRecruits)
        {
            var recruitLocation = (Location)locations.FirstOrDefault(x => x.Name == recruit.Name);
            var townPresenceAddress = recruitLocation.Address - Addresses.EventToTownFlagOffset;
            Memory.WriteBit(townPresenceAddress, recruitLocation.AddressBit, true);
        }

        // Clear town-presence flags (old range) for missing recruits
        var missingRecruits = Helpers.GetMissingRecruits(Client);
        foreach (var recruit in missingRecruits)
        {
            var recruitLocation = (Location)locations.FirstOrDefault(x => x.Name == recruit.Name);
            var townPresenceAddress = recruitLocation.Address - Addresses.EventToTownFlagOffset;
            Memory.WriteBit(townPresenceAddress, recruitLocation.AddressBit, false);
        }
    }
    public async Task Connect(ConnectClickedEventArgs args)
    {
        if (Client != null)
        {
            Client.Connected -= OnConnected;
            Client.Disconnected -= OnDisconnected;
        }
        GameClient client;
        var processHandler = new ProcessPickerWindow("duckstation");
        var result = await processHandler.ShowDialog<ProcessInfo?>(MainWindow);
        if (result != null)
        {
            client = new GameClient(result.ProcessName, result.PID);
        }
        else client = new GameClient("duckstation");
        var duckstationConnected = client.Connect();
        if (!duckstationConnected)
        {
            Log.Warning("Duckstation not running, open Duckstation and launch the game before connecting!");
            return;
        }
        Client = new ArchipelagoClient(client);

        PlatformMemory.GlobalOffset = PlatformMemory.GetDuckstationOffset();

        Client.Connected += OnConnected;
        Client.Disconnected += OnDisconnected;

        await Client.Connect(args.Host, "Digimon World");

        await Client.Login(args.Slot, !string.IsNullOrWhiteSpace(args.Password) ? args.Password : null);

        Helpers.DigimonTechniques = ReadTechniques();

#if DEBUG
        _ = Task.Run(async () =>
        {
            await Helpers.WaitForJijimonIntroAsync();
            var dumpPath = System.IO.Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.Desktop),
                "dw1_ram_dump.bin");
            Helpers.DumpPS1RAM(dumpPath);
        }).ConfigureAwait(false);
#endif

        var locations = Helpers.GetProsperityLocations();
        locations.AddRange(Helpers.GetDigimonCards());
        locations.AddRange(Helpers.GetChests());
        Client.LocationManager.EnableLocationsCondition = ()=> Helpers.IsInGame();

        Client.LocationManager.MonitorLocationsAsync(Client.CurrentSession, locations);
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
        Client.ItemManager.ItemReceived += OnItemReceived;

        //Is game started yet?
        if (!Client.CurrentSession.Locations.AllLocationsChecked.Any(x => x == 69003000))
        {
            _ = Task.Run(async () =>
            {
                try
                {
                    await Helpers.WaitForJijimonIntroAsync();
                    var startGameLocation = new Archipelago.Core.Models.Location() { Id = 69003000, Name = "Start Game" };
                    Client.CurrentSession.Locations.CompleteLocationChecks(startGameLocation.Id);
                }
                catch (Exception ex)
                {
                    Log.Logger.Error(ex.Message);
                }
            }).ConfigureAwait(false);
        }
        var recruitedLocations = new List<Archipelago.Core.Models.ILocation>();
        var acquiredRecruits = Helpers.GetAcquiredRecruits(Client);
        if (acquiredRecruits.Any())
        {
            var allLocations = Helpers.GetLocations();
            foreach (var recruit in acquiredRecruits)
            {
                var recruitLocation = allLocations.FirstOrDefault(x => x.Name == recruit.Name);
                recruitedLocations.Add(recruitLocation);
            }
            if (recruitedLocations.Any())
            {
                Client.LocationManager.MonitorLocationsAsync(Client.CurrentSession, recruitedLocations);
            }
        }
    }

    private void OnItemReceived(object? sender, ItemReceivedEventArgs args)
    {
        Log.Information($"Item Received: {JsonConvert.SerializeObject(args.Item)}");
        if (Helpers.APItems.Any(x => x.Id == args.Item.Id))
        {
            var item = Helpers.APItems.First(x => x.Id == args.Item.Id);
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
        else if (Helpers.DigimonRecruits.Any(x => x.Id == args.Item.Id))
        {
            var item = Helpers.DigimonRecruits.First(x => x.Id == args.Item.Id);
            var digimonRecruit = Helpers.GetLocations().Where(x => x.Name == item.Name).ToList();
            Client.LocationManager.MonitorLocationsAsync(Client.CurrentSession, digimonRecruit);
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
                new TextSpan(){Text = $"[{item.Id.ToString()}] -", TextColor = new SolidColorBrush(Color.FromRgb(255, 255, 255))},
                new TextSpan(){Text = $"{item.Name}", TextColor = new SolidColorBrush(Color.FromRgb(200, 255, 200))},
            });
        lock (_lockObject)
        {
            RxApp.MainThreadScheduler.Schedule(() =>
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

        if (Context.HintList.Any(x => x.TextSpans.Select(y => y.Text).SequenceEqual(newMessage)))
        {
            return; //Hint already in list
        }
        List<TextSpan> spans = new List<TextSpan>();
        foreach (var part in message.Parts)
        {
            spans.Add(new TextSpan() { Text = part.Text, TextColor = new SolidColorBrush(Color.FromRgb(part.Color.R, part.Color.G, part.Color.B)) });
        }
        lock (_lockObject)
        {
            RxApp.MainThreadScheduler.Schedule(() =>
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
}
