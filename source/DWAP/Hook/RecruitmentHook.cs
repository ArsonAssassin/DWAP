using Archipelago.Core.Util.Hook;
using Serilog;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DWAP.Hook
{
    public class RecruitmentHook
    {
        private FunctionHook _hook;
        private bool _isInstalled = false;
        public event EventHandler<RecruitmentEventArgs> DigimonRecruited;
        public bool Install()
        {
            Log.Debug("Installing Recruitment hook");
            if (_isInstalled)
            {
                Log.Warning("Recruitment hook is already installed");
                return true;
            }

            try
            {
                IntPtr functionAddress = (nint)Addresses.RecruitmentFunctionAddress;

                _hook = new FunctionHook(functionAddress, OnRecruitmentAttempt, hookSize: 5, executeOriginalInstructions: false);


                bool success = _hook.Install();

                if (success)
                {
                    _isInstalled = true;
                    Log.Debug("Recruitment hook installed successfully");
                }
                else
                {
                    Log.Error("Failed to install recruitment hook");
                }

                return success;
            }
            catch (Exception ex)
            {
                Log.Error($"Exception installing recruitment hook: {ex}");
                return false;
            }
        }
        private bool OnRecruitmentAttempt(HookContext context)
        {
            try
            {
                // Guesses for now
                int digimonId = context.Parameters[0].ToInt32();
                byte recruitedFlag = (byte)context.Parameters[1].ToInt32();

                Log.Debug($"Recruitment hook triggered: DigimonID={digimonId}, Flag={recruitedFlag}");

                context.UserData["digimonId"] = digimonId;
                context.UserData["recruitedFlag"] = recruitedFlag;
                DigimonRecruited?.Invoke(this, new RecruitmentEventArgs { DigimonId = digimonId });
                return true;
            }
            catch (Exception ex)
            {
                Log.Error($"Error in recruitment hook: {ex}");
                return true;
            }
        }
    }
}
