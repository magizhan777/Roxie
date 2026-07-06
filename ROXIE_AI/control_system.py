import os
import psutil
import pyautogui
import screen_brightness_control as sbc

from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


# ---------------------------
# OPEN APPLICATIONS
# ---------------------------

def open_notepad():
    os.system("start notepad")

def open_calculator():
    os.system("start calc")

def open_chrome():
    os.system("start chrome")

def open_explorer():
    os.system("start explorer")

def open_task_manager():
    os.system("start taskmgr")


# ---------------------------
# SCREENSHOT
# ---------------------------

def take_screenshot():
    img = pyautogui.screenshot()
    img.save("roxie_screenshot.png")


# ---------------------------
# SYSTEM POWER
# ---------------------------

def shutdown_pc():
    os.system("shutdown /s /t 1")

def restart_pc():
    os.system("shutdown /r /t 1")

def lock_pc():
    os.system("rundll32.exe user32.dll,LockWorkStation")


# ---------------------------
# BRIGHTNESS CONTROL
# ---------------------------

def set_brightness(percent):
    sbc.set_brightness(percent)

def set_brightness(percent):
    import screen_brightness_control as sbc
    sbc.set_brightness(percent)

def brightness_up():
    current = sbc.get_brightness()[0]
    sbc.set_brightness(current + 10)

def brightness_down():
    current = sbc.get_brightness()[0]
    sbc.set_brightness(current - 10)


# ---------------------------
# VOLUME CONTROL
# ---------------------------

def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None
    )
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume

def set_volume(percent):
    try:
        vol = get_volume_interface()
        vol.SetMasterVolumeLevelScalar(percent / 100.0, None)
    except Exception as e:
        print(f"Volume error: {e}")

def volume_up():
    vol = get_volume_interface()
    current = vol.GetMasterVolumeLevelScalar()
    new_vol = min(current + 0.1, 1.0)
    vol.SetMasterVolumeLevelScalar(new_vol, None)

def volume_down():
    vol = get_volume_interface()
    current = vol.GetMasterVolumeLevelScalar()
    new_vol = max(current - 0.1, 0.0)
    vol.SetMasterVolumeLevelScalar(new_vol, None)

def mute_volume():
    vol = get_volume_interface()
    vol.SetMute(1, None)


# ---------------------------
# BATTERY STATUS
# ---------------------------

def battery_status():

    battery = psutil.sensors_battery()

    if battery is None:
        return "Battery info not available"

    percent = battery.percent
    plugged = battery.power_plugged

    if plugged:
        return f"Battery is {percent} percent and charging"
    else:
        return f"Battery is {percent} percent"


# ---------------------------
# AIRPLANE MODE
# (Windows shortcut simulation)
# ---------------------------

def toggle_airplane_mode():

    pyautogui.hotkey("win", "a")
    pyautogui.sleep(1)
    pyautogui.press("tab", presses=5)
    pyautogui.press("enter")