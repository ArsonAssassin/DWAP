using System.Text;

namespace DWAP
{
    internal static class Program
    {
        [STAThread]
        static void Main()
        {
            ApplicationConfiguration.Initialize();
            Application.Run(new Form1());
            Encoding.RegisterProvider(CodePagesEncodingProvider.Instance);
        }

    }
}