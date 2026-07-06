import os
import pyautogui
import psutil
import webbrowser

# -----------------------------
# AUTO LEARN APPLICATIONS
# -----------------------------

def get_installed_apps():

    paths = [
        "C:\\Program Files",
        "C:\\Program Files (x86)"
    ]

    apps = {}

    for path in paths:

        for root, dirs, files in os.walk(path):

            for file in files:

                if file.endswith(".exe"):

                    name = file.replace(".exe","").lower()
                    apps[name] = os.path.join(root, file)

    return apps


apps_cache = get_installed_apps()


def open_any_app(name):

    name = name.lower()

    if name in apps_cache:
        os.startfile(apps_cache[name])
        return f"Opening {name}"

    return "initializing search..."


# -----------------------------
# FAST FILE SEARCH
# -----------------------------

def search_laptop(filename):

    matches = []

    for root, dirs, files in os.walk("C:\\"):

        for file in files:

            if filename.lower() in file.lower():
                matches.append(os.path.join(root,file))

            if len(matches) >= 5:
                break

    if matches:
        return matches
    else:
        return ["No files found"]


# -----------------------------
# MOUSE CONTROL
# -----------------------------

def move_mouse(x,y):

    pyautogui.moveTo(x,y)
    return "Mouse moved"


def mouse_click():

    pyautogui.click()
    return "Mouse clicked"


# -----------------------------
# KEYBOARD CONTROL
# -----------------------------

def type_text(text):

    pyautogui.write(text)
    return "Typing text"


def press_key(key):

    pyautogui.press(key)
    return f"Pressed {key}"


# -----------------------------
# SIMPLE TASK AUTOMATION
# -----------------------------

def open_youtube():
    webbrowser.open("https://www.youtube.com")
    return "Opening YouTube"


def open_google():
    webbrowser.open("https://www.google.com")
    return "Opening Google"

def open_website(name):
    url = f"https://www.{name}.com"
    webbrowser.open(url)
    return f"Opening {name}"