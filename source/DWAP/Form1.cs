using Archipelago.ePSXe;
using Archipelago.ePSXe.Models;
using Archipelago.ePSXe.Util;
using Newtonsoft.Json;
using System.Text;

namespace DWAP
{
    public partial class Form1 : Form
    {
        public static ArchipelagoClient Client { get; set; }
        public static List<DigimonWorldItem> Items { get; set; }
        public static List<Recruitment> RecruitList { get; set; }
        public Form1()
        {
            InitializeComponent();
            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);


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
            await Client.Connect(hostTextbox.Text, "Digimon World");
            // var locations = Helpers.GetLocations();
            var locations = GetRecruitmentLocations();
            locations.AddRange(Helpers.GetTemp());
            Client.PopulateLocations(locations);
            await Client.Login(slotTextbox.Text, !string.IsNullOrWhiteSpace(passwordTextbox.Text) ? passwordTextbox.Text : null);
            WriteLine("Connected to Archipelago");
            WriteLine($"Playing as {Client.CurrentSession.ConnectionInfo.Slot} playing {Client.CurrentSession.ConnectionInfo.Game}");
            timer1.Start();

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
                    else if(item.Name == "1000 Bits")
                    {
                        var currentCash = Memory.ReadInt(0x00B8C858);
                        var newCash = currentCash + 1000;
                        Memory.Write(0x00B8C858, newCash);
                    }
                }
            };
        }

        private List<Location> GetRecruitmentLocations()
        {
            var recruits = Helpers.GetRecruitment();
            var locations = Helpers.GetLocations();

            var result = new List<Location>();
            foreach(var recruit in  recruits)
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
            //EnsureRecruitment();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

            WriteLine("DWAP - Digimon world Archipelago Randomiser -- By ArsonAssassin --");
            WriteLine("Initialising collections...");
            Items = Helpers.GetItems();
            RecruitList = Helpers.GetRecruitment();
            WriteLine("Ready to connect!");
        }
    }
}
