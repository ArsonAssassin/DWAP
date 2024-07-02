using Archipelago.ePSXe;
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
            WriteLine("DWAP - Digimon world Archipelago Randomiser -- By ArsonAssassin --");
            WriteLine("Initialising collections...");
            Items = Helpers.GetItems();
            RecruitList = Helpers.GetRecruitment();
            WriteLine("Ready to connect!");
            
        }
        public void Connect()
        {
            ePSXeClient client = new ePSXeClient();
            var ePSXeConnected = client.Connect();
            if (!ePSXeConnected)
            {
                WriteLine("ePSXE not running, open ePSXe and launch the game before connecting!");
                return;
            }
            Client = new ArchipelagoClient();
            Client.Connect(hostTextbox.Text, "Digimon World").ConfigureAwait(false).GetAwaiter().GetResult();
            if (!client.IsConnected)
            {
                WriteLine("Could not connect to Archipelago, please check your settings and try again.");
                return;
            }
            var locations = Helpers.GetLocations();
            Client.PopulateLocations(locations);
            Client.Login(slotTextbox.Text).ConfigureAwait(false).GetAwaiter().GetResult();

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
                        EnsureRecruitment();
                    }
                }
            };
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
                Memory.WriteBit(digimon.Address, digimon.AddressBit, digimon.IsRecruited);
            }
        }

        public void WriteLine(string output)
        {
            outputTextbox.Text += output;
            outputTextbox.Text += System.Environment.NewLine;
        }

        private void connectbtn_Click(object sender, EventArgs e)
        {
            var valid = ValidateSettings();
            if (!valid)
            {
                WriteLine("Invalid settings, please check your input and try again.");
                return;
            }
            Connect();
        }
        private bool ValidateSettings()
        {
            var valid = !string.IsNullOrWhiteSpace(hostTextbox.Text) && !string.IsNullOrWhiteSpace(slotTextbox.Text);
            return valid;
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            EnsureRecruitment();
        }
    }
}
