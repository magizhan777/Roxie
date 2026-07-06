import os
import psutil
import subprocess
import pyautogui

# -----------------------------
# OPEN ANY APPLICATION
# -----------------------------

def open_application(app_name):

    try:
        os.system(f"start {app_name}")
        return f"Opening {app_name}"
    except:
        return "Application not found"


# -----------------------------
# SEARCH FILES ON COMPUTER
# -----------------------------

def search_file(filename):

    search_path = "C:\\"

    results = []

    for root, dirs, files in os.walk(search_path):

        for file in files:

            if filename.lower() in file.lower():
                results.append(os.path.join(root, file))

            if len(results) >= 5:
                break

    if results:
        return results
    else:
        return ["No file found"]


# -----------------------------
# SYSTEM USAGE
# -----------------------------

def cpu_usage():

    cpu = psutil.cpu_percent(interval=1)
    return f"CPU usage is {cpu} percent"


def ram_usage():

    ram = psutil.virtual_memory().percent
    return f"RAM usage is {ram} percent"


def battery_status():

    battery = psutil.sensors_battery()

    if battery:
        percent = battery.percent
        plugged = battery.power_plugged

        if plugged:
            return f"Battery is {percent} percent and charging"
        else:
            return f"Battery is {percent} percent"

    return "Battery information not available"


# -----------------------------
# WIFI CONTROL
# -----------------------------

def wifi_on():

    subprocess.run(
        "netsh interface set interface Wi-Fi enabled",
        shell=True
    )

    return "WiFi turned on"


def wifi_off():

    subprocess.run(
        "netsh interface set interface Wi-Fi disabled",
        shell=True
    )

    return "WiFi turned off"


# -----------------------------
# BLUETOOTH CONTROL
# -----------------------------

def bluetooth_on():

    pyautogui.hotkey("win", "a")
    pyautogui.sleep(1)
    pyautogui.press("tab", presses=6)
    pyautogui.press("enter")

    return "Bluetooth toggled"


def bluetooth_off():

    pyautogui.hotkey("win", "a")
    pyautogui.sleep(1)
    pyautogui.press("tab", presses=6)
    pyautogui.press("enter")

    return "Bluetooth toggled"