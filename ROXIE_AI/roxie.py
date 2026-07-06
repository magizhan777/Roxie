"""
╔══════════════════════════════════════════════════╗
║         J.A.R.V.I.S  —  IRON EDITION            ║
║   Just A Rather Very Intelligent System          ║
║   Powered by Ollama AI  |  Built for You         ║
╚══════════════════════════════════════════════════╝
"""

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import cv2
import re
import time
import json
import os
import pyautogui
import platform
import subprocess
import threading
import queue
import sys
import functools
import http.server
import socketserver
import ast
import operator
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
try:
    import tkinter as tk
    TK_AVAILABLE = True
except Exception:
    TK_AVAILABLE = False

# ─── Optional imports with graceful degradation ───────────────────────────────
try:
    import pythoncom
    PYTHONCOM_AVAILABLE = True
except ImportError:
    PYTHONCOM_AVAILABLE = False

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False

try:
    import pywhatkit
    PYWHATKIT_AVAILABLE = True
except ImportError:
    PYWHATKIT_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    import screen_brightness_control as sbc
    SBC_AVAILABLE = True
except ImportError:
    SBC_AVAILABLE = False

try:
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from ctypes import POINTER, cast
    from comtypes import CLSCTX_ALL
    PYCAW_AVAILABLE = True
except ImportError:
    PYCAW_AVAILABLE = False

# ─── System modules ───────────────────────────────────────────────────────────
from system_control import *
from control_system import *
from automation_system import *

# ─── Constants ────────────────────────────────────────────────────────────────
MEMORY_FILE   = "roxie_memory.json"
LOG_FILE      = "roxie_log.json"
CONFIG_FILE   = "roxie_config.json"
ASSISTANT_NAME = "Roxie"
WAKE_TOKEN    = "roxie"
WAKE_WORDS    = [
    "roxie",
    "roxy",
    "proxy",
    "oxy",
    "oxide",
    "toxic",
    "foxy",
    "boxy",
    "rocky",
    "roxyy",
    "roxi",
    "roxii",
    "roxey",
    "rosey",
    "rosie",
    "rosy",
    "rosi",
    "rowzy",
    "rowzie",
    "rory",
    "roary",
    "broxy",
    "croxy",
    "froxy",
    "droxy",
    "proxi",
    "proxies",
    "foxie",
    "boxie",
    "rockie",
    "rockey",
    "oxyy",
    "oxie",
    "roxxy",
    "roxe",
    "roksy",
    "rocksy",
    "rocks",
    "rose",
    "rashi",
    "raksi",
    "rakhi",
    "ruxi",
    "ruksy",
    "raw see",
    "rock see",
    "hey roxie",
    "ok roxie",
    "assistant",
]
DIRECT_COMMAND_HINTS = [
    "time", "date", "day", "system status", "battery", "cpu", "ram",
    "volume", "mute", "unmute", "brightness", "lock screen", "lock my",
    "screenshot", "camera", "what do you see", "weather", "timer",
    "calculate", "compute", "note", "notes", "health check", "alarm",
    "analyze screen", "read screen", "detect face", "list files",
    "open downloads", "open desktop", "open documents", "virtual keyboard",
    "keyboard press", "press key", "keyboard type", "retry microphone",
    "microphone test", "hand keyboard",
    "camera keyboard", "ai keyboard"
]
OWNER_NAME    = "Sir"
OLLAMA_URL    = "http://localhost:11434/api/generate"
OLLAMA_MODEL  = "llama3"
OLLAMA_TIMEOUT = 45
MAX_CONVERSATIONS = 10

# Local AI settings: Ollama runs on your machine, no cloud API key required.

# ─── Conversation history for multi-turn AI ───────────────────────────────────
conversation_history = []

# ─── Thread-safe speech queue ─────────────────────────────────────────────────
speech_queue = queue.Queue()
_tts_worker_started = False
_tts_lock = threading.Lock()
_dashboard_server = None
_dashboard_thread = None
LAST_RESPONSE = ""
PENDING_CONFIRMATION = None
NOTES_FILE = "roxie_notes.json"
ALARMS_FILE = "roxie_alarms.json"
ERROR_LOG_FILE = "roxie_errors.json"
_virtual_keyboard_thread = None
_virtual_keyboard_window = None
_virtual_keyboard_visible = False
_virtual_keyboard_text = ""
_virtual_keyboard_text_var = None

# ══════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════

DEFAULT_CONFIG = {
    "owner_name": "Sir",
    "voice_rate": 175,
    "voice_index": 0,
    "preferred_voice_keywords": [],
    "personality": "professional",
    "wake_sensitivity": "medium",
    "ai_model": OLLAMA_MODEL,
    "max_ai_tokens": 300,
}

def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            cfg = json.load(f)
        return {**DEFAULT_CONFIG, **cfg}
    return DEFAULT_CONFIG.copy()

def save_config(cfg: dict) -> None:
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

CONFIG = load_config()
if ("cl" + "aude") in str(CONFIG.get("ai_model", "")).lower():
    CONFIG["ai_model"] = OLLAMA_MODEL
    save_config(CONFIG)
OWNER_NAME = CONFIG["owner_name"]

# ══════════════════════════════════════════════════
#  MEMORY
# ══════════════════════════════════════════════════

def load_memory() -> dict:
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE) as f:
        return json.load(f)

def save_memory(data: dict) -> None:
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

def remember(key: str, value: str) -> None:
    mem = load_memory()
    mem[key] = value
    save_memory(mem)
    speak(f"Noted. I've stored that {key} is {value}, {OWNER_NAME}.")

def recall(key: str) -> str:
    mem = load_memory()
    if key in mem:
        return mem[key]
    return None

def forget(key: str) -> None:
    mem = load_memory()
    if key in mem:
        del mem[key]
        save_memory(mem)
        speak(f"I've cleared the record for '{key}', {OWNER_NAME}.")
    else:
        speak(f"I have no record of '{key}'.")

# ── Timetable helpers ─────────────────────────────

def set_schedule(scope: str, label: str, tasks: list) -> None:
    """scope: 'weekly' | 'monthly'"""
    mem = load_memory()
    key = f"{scope}_schedule"
    mem.setdefault(key, {})[label.lower()] = tasks
    save_memory(mem)
    speak(f"Schedule for {label} saved, {OWNER_NAME}.")

def get_schedule(scope: str, label: str) -> None:
    mem = load_memory()
    tasks = mem.get(f"{scope}_schedule", {}).get(label.lower())
    if tasks:
        speak(f"Your {scope} tasks for {label}: {', '.join(tasks)}.")
    else:
        speak(f"No {scope} schedule found for {label}.")

# ══════════════════════════════════════════════════
#  LOGGING
# ══════════════════════════════════════════════════

def log_interaction(user_input: str, response: str) -> None:
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "user": user_input,
        "roxie": response,
    }
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            logs = json.load(f)
    logs.append(entry)
    logs = logs[-500:]          # keep last 500 interactions
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

# ══════════════════════════════════════════════════
#  VOICE — speak()
# ══════════════════════════════════════════════════

def log_status(channel: str, message: str) -> None:
    print(f"[{channel.upper()}] {message}")


def log_error(message: str) -> None:
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "error": message,
    }
    logs = []
    if os.path.exists(ERROR_LOG_FILE):
        try:
            with open(ERROR_LOG_FILE) as f:
                logs = json.load(f)
        except Exception:
            logs = []
    logs.append(entry)
    with open(ERROR_LOG_FILE, "w") as f:
        json.dump(logs[-200:], f, indent=2)


def wait_for_speech() -> None:
    """Compatibility hook; speak() is currently blocking for reliability."""
    return


def _configure_tts_engine(engine):
    voices = engine.getProperty("voices")
    idx = CONFIG.get("voice_index", 0)
    selected_voice = None
    preferred = [v.lower() for v in CONFIG.get("preferred_voice_keywords", [])]
    if voices:
        for voice in voices:
            voice_text = f"{getattr(voice, 'name', '')} {getattr(voice, 'id', '')}".lower()
            if any(keyword in voice_text for keyword in preferred):
                selected_voice = voice
                break
        if selected_voice is None and 0 <= idx < len(voices):
            selected_voice = voices[idx]
    if selected_voice:
        engine.setProperty("voice", selected_voice.id)
    engine.setProperty("rate", CONFIG.get("voice_rate", 175))
    return selected_voice


def _speak_blocking(text: str) -> None:
    com_ready = False
    engine = None
    with _tts_lock:
        try:
            if PYTHONCOM_AVAILABLE:
                pythoncom.CoInitialize()
                com_ready = True
            engine = pyttsx3.init()
            _configure_tts_engine(engine)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            log_status("VOICE", f"TTS unavailable: {str(e)[:80]}")
        finally:
            if engine:
                try:
                    engine.stop()
                except Exception:
                    pass
            if com_ready:
                try:
                    pythoncom.CoUninitialize()
                except Exception:
                    pass


def _tts_worker() -> None:
    if PYTHONCOM_AVAILABLE:
        try:
            pythoncom.CoInitialize()
        except Exception as e:
            log_status("VOICE", f"COM initialization warning: {e}")

    while True:
        text = speech_queue.get()
        if text is None:
            speech_queue.task_done()
            break
        try:
            engine = pyttsx3.init()
            selected_voice = _configure_tts_engine(engine)
            if selected_voice:
                log_status("VOICE", f"Speaking with: {getattr(selected_voice, 'name', selected_voice.id)}")
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            log_status("VOICE", f"TTS error: {e}")
        finally:
            speech_queue.task_done()

    if PYTHONCOM_AVAILABLE:
        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass


def start_tts_worker() -> None:
    global _tts_worker_started
    if _tts_worker_started:
        return
    threading.Thread(target=_tts_worker, daemon=True, name="RoxieTTS").start()
    _tts_worker_started = True


def speak(text: str, log: bool = True) -> None:
    """Print and speak reliably before returning."""
    global LAST_RESPONSE
    if not text:
        return
    LAST_RESPONSE = text
    if log:
        log_status("AI", text)

    try:
        t = threading.Thread(target=_speak_blocking, args=(text,), daemon=True, name="RoxieSpeak")
        t.start()
        t.join()
    except Exception as e:
        log_status("VOICE", f"Unable to speak: {e}")

# ══════════════════════════════════════════════════
#  LOCAL AI - Ollama brain
# ══════════════════════════════════════════════════

SYSTEM_PROMPT = f"""You are Roxie, a sophisticated local AI assistant with a polished, professional personality.

Personality traits:
- Highly professional, articulate, and precise
- Subtly witty with dry British-style humor
- Always addresses the user as "{OWNER_NAME}"
- Concise responses (2-4 sentences max unless asked for detail)
- Never says "I cannot" — instead finds creative ways to help or explains limitations elegantly
- Uses phrases like "Right away", "Certainly", "Affirmative", "Understood"
- Occasionally references the user's mission or goals to show contextual awareness

Current date and time: {datetime.datetime.now().strftime('%A, %B %d %Y — %H:%M')}
System: {platform.system()} {platform.release()}

You have access to system controls. When the user asks for system tasks you cannot directly perform, acknowledge and guide them.
Keep responses short and spoken-word friendly — no markdown, no bullet points in responses."""


def _format_ollama_prompt(user_message: str, messages: list[dict]) -> str:
    history_text = ""
    for item in messages:
        role = "User" if item.get("role") == "user" else ASSISTANT_NAME
        history_text += f"{role}: {item.get('content', '')}\n"
    return f"{SYSTEM_PROMPT}\n\nConversation:\n{history_text}User: {user_message}\n{ASSISTANT_NAME}:"


def _trim_conversation_history() -> None:
    del conversation_history[:-MAX_CONVERSATIONS * 2]


def ask_ai(user_message: str, use_history: bool = True) -> str:
    """Send a message to local Ollama and return a spoken-friendly response."""
    global conversation_history

    if use_history:
        messages = conversation_history[-MAX_CONVERSATIONS * 2:]
    else:
        messages = []

    payload = {
        "model": CONFIG.get("ai_model", OLLAMA_MODEL),
        "prompt": _format_ollama_prompt(user_message, messages),
        "stream": False,
        "options": {
            "num_predict": CONFIG.get("max_ai_tokens", 300),
            "temperature": 0.7,
        },
    }
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=OLLAMA_TIMEOUT) as response:
            data = json.loads(response.read().decode("utf-8"))
        reply = data.get("response", "").strip()
        if not reply:
            reply = f"I received an empty response from the local model, {OWNER_NAME}."

        if use_history:
            conversation_history.append({"role": "user", "content": user_message})
            conversation_history.append({"role": "assistant", "content": reply})
            _trim_conversation_history()

        return reply

    except urllib.error.URLError:
        return f"My local AI core is offline, {OWNER_NAME}. Please start Ollama and make sure llama3 is installed."
    except TimeoutError:
        return f"The local AI took too long to respond, {OWNER_NAME}. Ollama may still be loading llama3."
    except Exception as e:
        return f"Something unexpected occurred in the local AI core, {OWNER_NAME}. {str(e)[:80]}"


def ai_quick(prompt: str) -> str:
    """Single-shot AI call, no history."""
    return ask_ai(prompt, use_history=False)

# ══════════════════════════════════════════════════
#  OBJECT DETECTION  (YOLOv3)
# ══════════════════════════════════════════════════

def detect_objects(duration: int = 10) -> None:
    speak("Activating visual sensors.")
    try:
        net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
        with open("coco.names") as f:
            classes = [l.strip() for l in f]

        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            speak("Visual sensors offline, unable to access camera.")
            return

        detected: dict[str, float] = {}
        end_time = time.time() + max(1, duration)
        last_frame = None
        window_name = "Roxie - Visual Analysis"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

        while time.time() < end_time:
            ret, frame = cap.read()
            if not ret:
                break
            seconds_left = max(0, int(end_time - time.time()) + 1)
            h, w, _ = frame.shape
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0,0,0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(output_layers)

            boxes, confidences, class_ids = [], [], []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    cid = scores.argmax()
                    conf = float(scores[cid])
                    if conf > 0.5:
                        cx, cy = int(detection[0]*w), int(detection[1]*h)
                        bw, bh = int(detection[2]*w), int(detection[3]*h)
                        boxes.append([cx-bw//2, cy-bh//2, bw, bh])
                        confidences.append(conf)
                        class_ids.append(cid)

            idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            for i in (idxs.flatten() if len(idxs) > 0 else []):
                label = classes[class_ids[i]]
                conf  = confidences[i]
                detected[label] = max(detected.get(label, 0), conf)
                x, y, bw, bh = boxes[i]
                cv2.rectangle(frame, (x, y), (x+bw, y+bh), (0, 230, 255), 2)
                cv2.putText(frame, f"{label} {conf:.0%}", (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 230, 255), 2)

            cv2.putText(frame, "ROXIE VISION ACTIVE", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 230, 255), 2)
            cv2.putText(frame, f"Scanning: {seconds_left}s", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 230, 255), 2)
            last_frame = frame
            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) == 27:
                break

        if last_frame is not None:
            hold_until = time.time() + 3
            cv2.putText(last_frame, "SCAN COMPLETE", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 230, 255), 2)
            while time.time() < hold_until:
                cv2.imshow(window_name, last_frame)
                if cv2.waitKey(50) == 27:
                    break

        cap.release()
        cv2.destroyAllWindows()

        if detected:
            top = sorted(detected, key=detected.get, reverse=True)[:5]
            keyboard_detect_action(top)
            summary = ", ".join(top)
            speak(f"Visual analysis complete. I can see: {summary}.")
            # Ask the local AI for interesting commentary.
            commentary = ai_quick(f"In one brief sentence, make an interesting observation about seeing these objects: {summary}. Be witty.")
            speak(commentary)
        else:
            speak("Visual scan complete. No recognizable objects detected in frame.")

    except FileNotFoundError:
        speak("YOLOv3 model files not found. Please ensure yolov3.weights, yolov3.cfg and coco.names are present.")

# ══════════════════════════════════════════════════
#  SYSTEM CONTROL  (volume, brightness, etc.)
# ══════════════════════════════════════════════════

def _set_volume_level(percent: int) -> tuple[bool, str]:
    percent = max(0, min(100, int(percent)))
    if PYCAW_AVAILABLE:
        com_ready = False
        try:
            if PYTHONCOM_AVAILABLE:
                pythoncom.CoInitialize()
                com_ready = True
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            vol = cast(interface, POINTER(IAudioEndpointVolume))
            vol.SetMasterVolumeLevelScalar(percent / 100.0, None)
            return True, f"Volume set to {percent} percent."
        except Exception as e:
            log_status("SYSTEM", f"Volume API error: {e}")
        finally:
            if com_ready:
                try:
                    pythoncom.CoUninitialize()
                except Exception:
                    pass

    try:
        pyautogui.press("volumemute")
        pyautogui.press("volumemute")
        pyautogui.press("volumedown", presses=50)
        pyautogui.press("volumeup", presses=max(1, percent // 2))
        return True, f"Volume adjusted near {percent} percent using keyboard controls."
    except Exception as e:
        return False, f"I could not change the volume automatically. Error: {str(e)[:80]}"


def _change_volume(delta: int) -> str:
    key = "volumeup" if delta > 0 else "volumedown"
    presses = max(1, abs(delta) // 2)
    try:
        pyautogui.press(key, presses=presses)
        return "Volume increased." if delta > 0 else "Volume decreased."
    except Exception as e:
        return f"I could not adjust the volume. Error: {str(e)[:80]}"


def _toggle_mute() -> str:
    try:
        pyautogui.press("volumemute")
        return "Audio mute toggled."
    except Exception as e:
        return f"I could not toggle mute. Error: {str(e)[:80]}"


def _set_mute(muted: bool) -> str:
    if PYCAW_AVAILABLE:
        com_ready = False
        try:
            if PYTHONCOM_AVAILABLE:
                pythoncom.CoInitialize()
                com_ready = True
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            vol = cast(interface, POINTER(IAudioEndpointVolume))
            vol.SetMute(1 if muted else 0, None)
            return "Audio muted." if muted else "Audio unmuted."
        except Exception as e:
            log_status("SYSTEM", f"Mute API error: {e}")
        finally:
            if com_ready:
                try:
                    pythoncom.CoUninitialize()
                except Exception:
                    pass
    return _toggle_mute()


def _lock_workstation() -> str:
    try:
        if platform.system().lower() == "windows":
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], check=False)
        else:
            lock_pc()
        return "Locking workstation."
    except Exception as e:
        return f"I could not lock the workstation. Error: {str(e)[:80]}"

def _set_brightness_level(percent: int) -> None:
    if SBC_AVAILABLE:
        try:
            sbc.set_brightness(percent)
        except Exception as e:
            print(f"[Brightness Error] {e}")
    else:
        speak("Brightness control not available on this system.")

def open_windows_setting(uri: str) -> None:
    try:
        os.startfile(uri)
    except Exception as e:
        log_status("SYSTEM", f"Could not open Windows settings page {uri}: {e}")


def _keyboard_press(label: str) -> None:
    global _virtual_keyboard_text
    key_map = {
        "SPACE": "space",
        "ENTER": "enter",
        "BACK": "backspace",
        "TAB": "tab",
        "ESC": "esc",
        "CTRL": "ctrl",
        "ALT": "alt",
        "SHIFT": "shift",
        "WIN": "win",
        "CAPS": "capslock",
        "DEL": "delete",
    }
    key = key_map.get(label.upper(), label.lower())
    pyautogui.press(key)

    if label.upper() == "BACK":
        _virtual_keyboard_text = _virtual_keyboard_text[:-1]
    elif label.upper() == "SPACE":
        _virtual_keyboard_text += " "
    elif label.upper() == "ENTER":
        _virtual_keyboard_text += "\n"
    elif len(label) == 1:
        _virtual_keyboard_text += label.lower()

    if _virtual_keyboard_text_var is not None:
        try:
            _virtual_keyboard_text_var.set(_virtual_keyboard_text[-120:])
        except Exception:
            pass


def _virtual_keyboard_ui() -> None:
    global _virtual_keyboard_window, _virtual_keyboard_visible, _virtual_keyboard_text_var
    if not TK_AVAILABLE:
        log_status("SYSTEM", "Tkinter is not available for the virtual keyboard.")
        return

    root = tk.Tk()
    _virtual_keyboard_window = root
    _virtual_keyboard_visible = True
    root.title("Roxie Virtual Keyboard")
    root.attributes("-topmost", True)
    root.configure(bg="#07131c")

    _virtual_keyboard_text_var = tk.StringVar(value=_virtual_keyboard_text)
    display = tk.Label(
        root,
        textvariable=_virtual_keyboard_text_var,
        anchor="w",
        justify="left",
        width=58,
        height=3,
        bg="#00131f",
        fg="#dff8ff",
        font=("Consolas", 12),
        relief=tk.GROOVE,
        padx=8,
        pady=6,
    )
    display.pack(padx=8, pady=(8, 5), fill=tk.X)

    rows = [
        list("1234567890"),
        list("QWERTYUIOP"),
        list("ASDFGHJKL"),
        list("ZXCVBNM"),
        ["TAB", "SPACE", "ENTER", "BACK", "ESC"],
    ]

    def press(label):
        try:
            _keyboard_press(label)
        except Exception as e:
            log_status("SYSTEM", f"Virtual key failed: {e}")

    for r, row in enumerate(rows):
        frame = tk.Frame(root, bg="#07131c")
        frame.pack(padx=8, pady=3)
        for label in row:
            width = 8 if label in ["SPACE", "ENTER", "BACK"] else 4
            btn = tk.Button(
                frame,
                text=label,
                width=width,
                height=2,
                bg="#0e3145",
                fg="#dff8ff",
                activebackground="#00a6d6",
                command=lambda value=label: press(value),
            )
            btn.pack(side=tk.LEFT, padx=2)

    def on_close():
        global _virtual_keyboard_visible, _virtual_keyboard_window, _virtual_keyboard_text_var
        _virtual_keyboard_visible = False
        _virtual_keyboard_window = None
        _virtual_keyboard_text_var = None
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


def show_virtual_keyboard() -> str:
    global _virtual_keyboard_thread, _virtual_keyboard_visible
    if _virtual_keyboard_visible:
        return "Virtual keyboard is already open."
    if not TK_AVAILABLE:
        return "Virtual keyboard is not available because Tkinter is missing."
    _virtual_keyboard_thread = threading.Thread(target=_virtual_keyboard_ui, daemon=True, name="RoxieVirtualKeyboard")
    _virtual_keyboard_thread.start()
    return "Virtual keyboard opened."


def close_virtual_keyboard() -> str:
    global _virtual_keyboard_visible, _virtual_keyboard_window
    if not _virtual_keyboard_window:
        return "Virtual keyboard is not open."
    try:
        _virtual_keyboard_window.after(0, _virtual_keyboard_window.destroy)
    except Exception:
        pass
    _virtual_keyboard_window = None
    _virtual_keyboard_visible = False
    return "Virtual keyboard closed."


def virtual_keyboard_command(cmd: str) -> str:
    if any(k in cmd for k in ["open virtual keyboard", "show virtual keyboard", "keyboard on"]):
        return show_virtual_keyboard()
    if any(k in cmd for k in ["close virtual keyboard", "hide virtual keyboard", "keyboard off"]):
        return close_virtual_keyboard()
    if m := re.search(r"(?:keyboard press|press key|press) (.+)", cmd):
        key = m.group(1).strip()
        _keyboard_press(key)
        return f"Pressed {key}."
    if m := re.search(r"(?:keyboard type|type text|type) (.+)", cmd):
        text = m.group(1)
        pyautogui.write(text, interval=0.03)
        return "Typed text."
    return "Virtual keyboard command not understood."


def keyboard_detect_action(detected_labels: list[str]) -> None:
    labels = {label.lower() for label in detected_labels}
    if "keyboard" in labels:
        speak("Keyboard detected. Opening virtual keyboard.")
        show_virtual_keyboard()


HAND_KEYBOARD_LAYOUT = [
    list("1234567890"),
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    list("ZXCVBNM"),
    ["SPACE", "BACK", "ENTER"],
]


def _draw_hand_keyboard(frame):
    h, w, _ = frame.shape
    key_boxes = []
    key_w = max(42, w // 13)
    key_h = 48
    start_y = h - (len(HAND_KEYBOARD_LAYOUT) * (key_h + 8)) - 20

    for row_index, row in enumerate(HAND_KEYBOARD_LAYOUT):
        row_width = sum((key_w * 3 if key == "SPACE" else key_w * 2 if key in ["BACK", "ENTER"] else key_w) for key in row)
        row_width += (len(row) - 1) * 6
        x = max(8, (w - row_width) // 2)
        y = start_y + row_index * (key_h + 8)
        for key in row:
            width = key_w * 3 if key == "SPACE" else key_w * 2 if key in ["BACK", "ENTER"] else key_w
            x2, y2 = x + width, y + key_h
            cv2.rectangle(frame, (x, y), (x2, y2), (0, 230, 255), 2)
            cv2.putText(frame, key, (x + 8, y + 31), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 230, 255), 2)
            key_boxes.append((key, x, y, x2, y2))
            x = x2 + 6
    return key_boxes


def _key_at_point(key_boxes, x, y):
    for key, x1, y1, x2, y2 in key_boxes:
        if x1 <= x <= x2 and y1 <= y <= y2:
            return key
    return None


def hand_control_virtual_keyboard(duration: int = 60) -> str:
    try:
        import mediapipe as mp
    except Exception:
        show_virtual_keyboard()
        return "Hand control needs mediapipe. I opened the normal virtual keyboard. Install hand tracking with: pip install mediapipe"

    show_virtual_keyboard()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Camera is not available for hand keyboard control."

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.65, min_tracking_confidence=0.65)
    last_key = None
    hover_started = 0
    pressed_at = 0
    last_pressed = ""
    end_time = time.time() + duration
    window_name = "Roxie AI Hand Keyboard"

    try:
        while time.time() < end_time:
            ok, frame = cap.read()
            if not ok:
                break
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            cv2.rectangle(frame, (10, 10), (w - 10, 92), (0, 19, 31), -1)
            cv2.rectangle(frame, (10, 10), (w - 10, 92), (0, 230, 255), 2)
            preview = _virtual_keyboard_text.replace("\n", " ")[-70:]
            cv2.putText(frame, "TEXT:", (24, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 230, 255), 2)
            cv2.putText(frame, preview or "(empty)", (110, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (220, 248, 255), 2)
            cv2.putText(frame, f"Last key: {last_pressed or '-'}", (24, 74), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 80), 2)

            key_boxes = _draw_hand_keyboard(frame)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            current_key = None
            if result.multi_hand_landmarks:
                hand = result.multi_hand_landmarks[0]
                fingertip = hand.landmark[8]
                fx, fy = int(fingertip.x * w), int(fingertip.y * h)
                cv2.circle(frame, (fx, fy), 12, (0, 255, 80), -1)
                current_key = _key_at_point(key_boxes, fx, fy)

                if current_key:
                    cv2.putText(frame, f"Hover: {current_key}", (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 80), 2)
                    if current_key != last_key:
                        last_key = current_key
                        hover_started = time.time()
                    elif time.time() - hover_started > 0.65 and time.time() - pressed_at > 0.9:
                        _keyboard_press(current_key)
                        last_pressed = current_key
                        pressed_at = time.time()
                        cv2.putText(frame, f"Pressed: {current_key}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 80), 2)
                else:
                    last_key = None
                    hover_started = 0

            cv2.putText(frame, "Point index finger at a key. Hold to press. ESC exits.", (10, h - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 230, 255), 2)
            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) == 27:
                break
    finally:
        cap.release()
        hands.close()
        cv2.destroyWindow(window_name)

    return "Hand keyboard control closed."

def system_info() -> str:
    if not PSUTIL_AVAILABLE:
        return "System monitoring libraries not installed."
    cpu  = psutil.cpu_percent(interval=0.5)
    ram  = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    info = (
        f"CPU at {cpu}%. "
        f"RAM usage {ram.percent}%, {ram.available // (1024**3)} gigabytes free. "
        f"Disk usage {disk.percent}%."
    )
    if hasattr(psutil, "sensors_battery"):
        batt = psutil.sensors_battery()
        if batt:
            info += f" Battery at {batt.percent:.0f}%{', charging' if batt.power_plugged else ''}."
    return info


def health_check() -> str:
    checks = [
        "Ollama endpoint configured",
        f"Text to speech {'available' if PYTHONCOM_AVAILABLE else 'available without pythoncom'}",
        f"System monitor {'available' if PSUTIL_AVAILABLE else 'missing psutil'}",
        f"Brightness control {'available' if SBC_AVAILABLE else 'not available'}",
        f"Advanced volume control {'available' if PYCAW_AVAILABLE else 'using keyboard fallback'}",
    ]
    return ". ".join(checks) + "."


def load_notes() -> list:
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE) as f:
            return json.load(f)
    except Exception:
        return []


def save_notes(notes: list) -> None:
    with open(NOTES_FILE, "w") as f:
        json.dump(notes[-100:], f, indent=2)


def add_note(text: str) -> str:
    notes = load_notes()
    notes.append({
        "timestamp": datetime.datetime.now().isoformat(),
        "note": text,
    })
    save_notes(notes)
    return "Note saved."


def list_notes() -> str:
    notes = load_notes()
    if not notes:
        return "You have no saved notes."
    recent = [n.get("note", "") for n in notes[-5:]]
    return "Your recent notes are: " + "; ".join(recent)


def clear_notes() -> str:
    save_notes([])
    return "All notes cleared."


SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def safe_calculate(expr: str) -> str:
    def _eval(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in SAFE_OPERATORS:
            return SAFE_OPERATORS[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in SAFE_OPERATORS:
            return SAFE_OPERATORS[type(node.op)](_eval(node.operand))
        raise ValueError("Unsupported calculation")

    try:
        expr = expr.lower()
        replacements = {
            "plus": "+",
            "add": "+",
            "minus": "-",
            "subtract": "-",
            "times": "*",
            "time": "*",
            "x": "*",
            "into": "*",
            "cross": "*",
            "star": "*",
            "multiply": "*",
            "multiplied by": "*",
            "divide by": "/",
            "divided by": "/",
            "over": "/",
        }
        for word, symbol in replacements.items():
            expr = re.sub(rf"\b{re.escape(word)}\b", symbol, expr)
        expr = re.sub(r"[^0-9+\-*/().\s]", " ", expr)
        expr = re.sub(r"\s+", " ", expr).strip()
        tree = ast.parse(expr, mode="eval")
        result = _eval(tree.body)
        return f"The answer is {result}."
    except Exception:
        return "I could not calculate that expression."


def load_alarms() -> list:
    if not os.path.exists(ALARMS_FILE):
        return []
    try:
        with open(ALARMS_FILE) as f:
            return json.load(f)
    except Exception:
        return []


def save_alarms(alarms: list) -> None:
    with open(ALARMS_FILE, "w") as f:
        json.dump(alarms[-100:], f, indent=2)


def schedule_alarm_at(target: datetime.datetime, label: str = "alarm") -> str:
    now = datetime.datetime.now()
    if target <= now:
        target += datetime.timedelta(days=1)
    alarms = load_alarms()
    alarm = {
        "time": target.isoformat(),
        "label": label,
        "active": True,
    }
    alarms.append(alarm)
    save_alarms(alarms)

    def _done():
        speak(f"Alarm: {label}.")

    threading.Timer(max(1, (target - now).total_seconds()), _done).start()
    return f"Alarm set for {target.strftime('%I:%M %p')}."


def restore_alarms() -> None:
    now = datetime.datetime.now()
    alarms = load_alarms()
    active = []
    for alarm in alarms:
        if not alarm.get("active", True):
            continue
        try:
            target = datetime.datetime.fromisoformat(alarm["time"])
        except Exception:
            continue
        if target <= now:
            continue
        active.append(alarm)

        def _done(label=alarm.get("label", "alarm")):
            speak(f"Alarm: {label}.")

        threading.Timer(max(1, (target - now).total_seconds()), _done).start()
    save_alarms(active)


def parse_alarm_command(cmd: str) -> str | None:
    if m := re.search(r"(?:set alarm|alarm) (?:for|at)?\s*(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", cmd):
        hour = int(m.group(1))
        minute = int(m.group(2) or 0)
        meridian = m.group(3)
        if meridian == "pm" and hour < 12:
            hour += 12
        if meridian == "am" and hour == 12:
            hour = 0
        now = datetime.datetime.now()
        target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        return schedule_alarm_at(target)
    return None


def list_alarms() -> str:
    alarms = load_alarms()
    if not alarms:
        return "No alarms are saved."
    labels = []
    for alarm in alarms[-5:]:
        try:
            t = datetime.datetime.fromisoformat(alarm["time"]).strftime("%I:%M %p")
        except Exception:
            t = "unknown time"
        labels.append(f"{alarm.get('label', 'alarm')} at {t}")
    return "Saved alarms: " + "; ".join(labels)


def clear_alarms() -> str:
    save_alarms([])
    return "All saved alarms cleared."


def start_timer(seconds: int, label: str = "timer") -> str:
    seconds = max(1, min(seconds, 24 * 60 * 60))

    def _done():
        speak(f"Timer complete: {label}.")

    threading.Timer(seconds, _done).start()
    if seconds < 60:
        return f"Timer set for {seconds} seconds."
    return f"Timer set for {seconds // 60} minutes."


def parse_duration(text: str) -> int | None:
    if m := re.search(r"(\d+)\s*(second|seconds|sec|secs)", text):
        return int(m.group(1))
    if m := re.search(r"(\d+)\s*(minute|minutes|min|mins)", text):
        return int(m.group(1)) * 60
    if m := re.search(r"(\d+)\s*(hour|hours)", text):
        return int(m.group(1)) * 3600
    return None


def get_weather(place: str = "") -> str:
    query = place.strip() or ""
    url = f"https://wttr.in/{urllib.parse.quote(query)}?format=3"
    try:
        with urllib.request.urlopen(url, timeout=8) as response:
            return response.read().decode("utf-8").strip()
    except Exception:
        return "I could not reach the weather service right now."


def analyze_screen() -> str:
    try:
        img = pyautogui.screenshot()
        path = f"roxie_screen_{int(time.time())}.png"
        img.save(path)
        try:
            import pytesseract
            text = pytesseract.image_to_string(img).strip()
            if text:
                return f"I captured the screen. Visible text includes: {text[:400]}"
        except Exception:
            pass
        return f"I captured the screen as {path}. OCR is not installed. To enable screen text reading, install pytesseract and the Tesseract Windows app."
    except Exception as e:
        log_error(f"Screen analysis failed: {e}")
        return f"I could not analyze the screen. Error: {str(e)[:80]}"


def analyze_web_page(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Roxie/1.0"})
        with urllib.request.urlopen(request, timeout=12) as response:
            html = response.read(500000).decode("utf-8", errors="ignore")
        title = ""
        if m := re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S):
            title = re.sub(r"\s+", " ", re.sub(r"<.*?>", "", m.group(1))).strip()
        text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.I | re.S)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        prompt = f"Summarize this web page briefly. Title: {title}. Text: {text[:3000]}"
        return ask_ai(prompt, use_history=False)
    except Exception as e:
        log_error(f"Page analysis failed: {e}")
        return f"I could not analyze that page. Error: {str(e)[:80]}"


def detect_faces(duration: int = 10) -> str:
    try:
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        face_cascade = cv2.CascadeClassifier(cascade_path)
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "Camera is not available."
        window_name = "Roxie - Face Detection"
        end_time = time.time() + duration
        max_faces = 0
        while time.time() < end_time:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.2, 5)
            max_faces = max(max_faces, len(faces))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 230, 255), 2)
            cv2.putText(frame, f"Faces: {len(faces)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 230, 255), 2)
            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
        return f"I detected up to {max_faces} face{'s' if max_faces != 1 else ''}."
    except Exception as e:
        log_error(f"Face detection failed: {e}")
        return f"Face detection failed. Error: {str(e)[:80]}"


def file_manager(command: str) -> str:
    base = Path.home()
    if "desktop" in command:
        base = Path.home() / "Desktop"
    elif "downloads" in command:
        base = Path.home() / "Downloads"
    elif "documents" in command:
        base = Path.home() / "Documents"
    if "open" in command:
        try:
            os.startfile(str(base))
            return f"Opened {base.name}."
        except Exception as e:
            return f"I could not open that folder. Error: {str(e)[:80]}"
    try:
        items = list(base.iterdir())[:10]
        if not items:
            return f"{base.name} is empty."
        return f"{base.name} contains: " + ", ".join(p.name for p in items)
    except Exception as e:
        return f"I could not read that folder. Error: {str(e)[:80]}"


def automation_command(cmd: str) -> str:
    try:
        if m := re.search(r"type (.+)", cmd):
            pyautogui.write(m.group(1), interval=0.02)
            return "Typed."
        if m := re.search(r"press (.+)", cmd):
            pyautogui.press(m.group(1).strip())
            return f"Pressed {m.group(1).strip()}."
        if "click" in cmd:
            pyautogui.click()
            return "Clicked."
        if "scroll up" in cmd:
            pyautogui.scroll(5)
            return "Scrolled up."
        if "scroll down" in cmd:
            pyautogui.scroll(-5)
            return "Scrolled down."
    except Exception as e:
        return f"Automation failed. Error: {str(e)[:80]}"
    return "I did not understand that automation command."

# ══════════════════════════════════════════════════
#  TEXT PROCESSING
# ══════════════════════════════════════════════════

def clean(text: str) -> str:
    return re.sub(r"[^\w\s]", "", text.lower()).strip()

def normalize_wake(text: str) -> str:
    for w in WAKE_WORDS:
        text = re.sub(rf"\b{re.escape(w)}\b", WAKE_TOKEN, text)
    return text

def extract_after(text: str, *keywords) -> str:
    for kw in keywords:
        if kw in text:
            return text.split(kw, 1)[1].strip()
    return ""

# ══════════════════════════════════════════════════
#  COMMAND ROUTER
# ══════════════════════════════════════════════════

def route_command(raw: str) -> None:
    """Intelligent command routing with local AI as the ultimate fallback."""
    global PENDING_CONFIRMATION
    cmd = clean(raw)
    raw_clean = raw.lower().strip()
    log_status("SYSTEM", f"Command routed: {cmd}")

    if PENDING_CONFIRMATION:
        if cmd in ["yes", "confirm", "do it", "proceed"]:
            action = PENDING_CONFIRMATION
            PENDING_CONFIRMATION = None
            action()
            return
        if cmd in ["no", "cancel", "stop", "never mind"]:
            PENDING_CONFIRMATION = None
            speak("Cancelled.")
            return

    if any(k in cmd for k in ["exit", "shutdown roxie", "close roxie", "goodbye", "quit"]):
        farewell = ask_ai(f"Say a brief, witty goodbye to {OWNER_NAME} as Roxie would.")
        speak(farewell)
        sys.exit(0)

    if any(k in cmd for k in ["retry microphone", "reconnect microphone", "reload microphone", "mic test", "microphone test"]):
        speak(retry_microphone())
        return

    if re.search(r"\d+\s*(?:plus|minus|times|into|cross|star|x|multiply|divide|over|\+|\-|\*|/)\s*\d+", raw_clean):
        speak(safe_calculate(raw_clean))
        return

    if any(k in cmd for k in ["health check", "diagnostics", "system check", "roxie status"]):
        speak(health_check())
        return

    if m := re.search(r"(?:take note|add note|note this|remember note) (.+)", cmd):
        speak(add_note(m.group(1).strip()))
        return

    if any(k in cmd for k in ["show notes", "read notes", "list notes"]):
        speak(list_notes())
        return

    if any(k in cmd for k in ["clear notes", "delete notes"]):
        speak(clear_notes())
        return

    if m := re.search(r"(?:calculate|compute|what is|activate)\s+(.+)", raw_clean):
        speak(safe_calculate(m.group(1)))
        return

    if "timer" in cmd or "remind me" in cmd:
        seconds = parse_duration(cmd)
        if seconds:
            label = re.sub(r"set|start|timer|remind me|in \d+ \w+|for \d+ \w+", "", cmd).strip() or "timer"
            speak(start_timer(seconds, label))
        else:
            speak("Please tell me the timer duration, such as 5 minutes or 30 seconds.")
        return

    if "weather" in cmd:
        place = re.sub(r"weather|in|for|at", "", cmd).strip()
        speak(get_weather(place))
        return

    if any(k in cmd for k in ["analyze screen", "read screen", "screen ocr", "what is on my screen"]):
        speak(analyze_screen())
        return

    if m := re.search(r"(?:analyze page|summarize page|read website|analyze website) (.+)", cmd):
        speak(analyze_web_page(m.group(1).strip()))
        return

    if any(k in cmd for k in ["detect face", "face detection", "scan faces"]):
        speak(detect_faces())
        return

    if any(k in cmd for k in ["list files", "open downloads", "open desktop", "open documents", "show downloads", "show desktop", "show documents"]):
        speak(file_manager(cmd))
        return

    if any(k in cmd for k in ["hand keyboard", "camera keyboard", "ai keyboard", "control keyboard with hand"]):
        speak(hand_control_virtual_keyboard())
        return

    if any(k in cmd for k in ["virtual keyboard", "keyboard on", "keyboard off", "keyboard press", "press key", "keyboard type"]):
        speak(virtual_keyboard_command(cmd))
        return

    if any(k in cmd for k in ["click", "scroll up", "scroll down", "press ", "type "]):
        speak(automation_command(cmd))
        return

    if "list alarms" in cmd or "show alarms" in cmd:
        speak(list_alarms())
        return

    if "clear alarms" in cmd or "delete alarms" in cmd:
        speak(clear_alarms())
        return

    if "alarm" in cmd:
        response = parse_alarm_command(cmd)
        speak(response or "Please say the alarm time, such as set alarm for 7:30 AM.")
        return

    # ── MEMORY ────────────────────────────────────
    if m := re.search(r"remember (?:that )?(.+?) is (.+)", cmd):
        remember(m.group(1).strip(), m.group(2).strip())
        return

    if m := re.search(r"(?:forget|delete|clear) (.+)", cmd):
        forget(m.group(1).strip())
        return

    if m := re.search(r"(?:what is|recall|remember) (.+)", cmd):
        key = m.group(1).strip()
        val = recall(key)
        if val:
            speak(f"{key} is {val}, {OWNER_NAME}.")
        else:
            reply = ask_ai(raw)
            speak(reply)
            log_interaction(raw, reply)
        return

    # ── SCHEDULES ─────────────────────────────────
    if m := re.search(r"set (weekly|monthly) (.+?) (.+)", cmd):
        scope, label, task_str = m.groups()
        tasks = [t.strip() for t in task_str.split(",")]
        set_schedule(scope, label, tasks)
        return

    if m := re.search(r"(weekly|monthly) schedule (?:for )?(.+)", cmd):
        get_schedule(m.group(1), m.group(2))
        return

    # ── TIME & DATE ───────────────────────────────
    if "time" in cmd and "what" in cmd or cmd == "time":
        speak(f"The time is {datetime.datetime.now().strftime('%I:%M %p')}, {OWNER_NAME}.")
        return

    if "date" in cmd or "day" in cmd:
        speak(f"Today is {datetime.datetime.now().strftime('%A, %B %d %Y')}.")
        return

    # ── SYSTEM INFO ───────────────────────────────
    if any(k in cmd for k in ["system status", "system info", "cpu", "ram", "battery", "how is the system"]):
        info = system_info()
        speak(info)
        return

    # ── VOLUME ────────────────────────────────────
    if "volume settings" in cmd or "sound settings" in cmd or "audio settings" in cmd:
        open_windows_setting("ms-settings:sound")
        speak("Sound settings are open.")
        return

    if m := re.search(r"(?:set )?volume (?:to )?(\d+)", cmd):
        lvl = int(m.group(1))
        ok, message = _set_volume_level(lvl)
        speak(message)
        return

    if any(k in cmd for k in ["volume up", "increase volume", "raise volume", "turn volume up"]):
        speak(_change_volume(10))
        return

    if any(k in cmd for k in ["volume down", "decrease volume", "lower volume", "turn volume down"]):
        speak(_change_volume(-10))
        return

    if "unmute" in cmd:
        speak(_set_mute(False))
        return

    if "mute" in cmd:
        speak(_set_mute(True))
        return

    # ── BRIGHTNESS ────────────────────────────────
    if "bluetooth" in cmd:
        if any(k in cmd for k in ["turn on", "enable", "switch on", "turn off", "disable", "switch off", "toggle"]):
            try:
                bluetooth_on()
                speak("I sent the Bluetooth toggle command and opened the Bluetooth panel for confirmation.")
            except Exception as e:
                log_status("SYSTEM", f"Bluetooth shortcut failed: {e}")
                speak("I could not toggle Bluetooth automatically, so I opened the Bluetooth settings panel.")
            open_windows_setting("ms-settings:bluetooth")
            return

        open_windows_setting("ms-settings:bluetooth")
        speak("Bluetooth settings are open.")
        return

    if "airplane mode" in cmd or "aeroplane mode" in cmd:
        if "toggle" in cmd:
            try:
                toggle_airplane_mode()
                speak("I sent the airplane mode toggle command. Please confirm the current state in Quick Settings.")
            except Exception as e:
                log_status("SYSTEM", f"Airplane mode shortcut failed: {e}")
                speak("I could not toggle airplane mode automatically, so I opened the airplane mode settings panel.")
            open_windows_setting("ms-settings:network-airplanemode")
            return

        open_windows_setting("ms-settings:network-airplanemode")
        speak("I opened airplane mode settings. Windows does not reliably allow normal Python to force this exact switch on or off.")
        return

    if m := re.search(r"(?:set )?brightness (?:to )?(\d+)", cmd):
        lvl = int(m.group(1))
        _set_brightness_level(lvl)
        speak(f"Display brightness set to {lvl} percent.")
        return

    if "brightness up" in cmd:
        if SBC_AVAILABLE:
            cur = sbc.get_brightness()[0]
            _set_brightness_level(min(100, cur + 15))
        speak("Brightness increased.")
        return

    if "brightness down" in cmd:
        if SBC_AVAILABLE:
            cur = sbc.get_brightness()[0]
            _set_brightness_level(max(0, cur - 15))
        speak("Brightness decreased.")
        return

    # ── COMPUTER POWER ────────────────────────────
    if "shutdown" in cmd:
        def _confirmed_shutdown():
            speak(f"Initiating system shutdown. Goodbye, {OWNER_NAME}.")
            time.sleep(2)
            shutdown_pc()
        PENDING_CONFIRMATION = _confirmed_shutdown
        speak("Please confirm shutdown by saying yes or cancel.")
        return

    if "restart" in cmd or "reboot" in cmd:
        def _confirmed_restart():
            speak("Restarting system.")
            restart_pc()
        PENDING_CONFIRMATION = _confirmed_restart
        speak("Please confirm restart by saying yes or cancel.")
        return

    if "lock" in cmd and any(k in cmd for k in ["computer", "screen", "pc", "workstation", "windows", "device", "laptop"]):
        speak(_lock_workstation())
        return

    if any(k in cmd for k in ["windows security", "security settings", "virus protection", "defender settings"]):
        open_windows_setting("windowsdefender:")
        speak("Windows Security is open.")
        return

    # ── SCREENSHOT ────────────────────────────────
    if "screenshot" in cmd or "capture screen" in cmd:
        fname = f"roxie_capture_{int(time.time())}.png"
        pyautogui.screenshot().save(fname)
        speak(f"Screen captured and saved as {fname}.")
        return

    # ── OPEN APPS ────────────────────────────────
    if m := re.search(r"open (.+)", cmd):
        app = m.group(1).strip()
        # Check known websites first
        sites = {"youtube": "https://youtube.com", "google": "https://google.com",
                 "gmail": "https://mail.google.com", "github": "https://github.com",
                 "netflix": "https://netflix.com", "spotify": "https://open.spotify.com"}
        if app in sites:
            speak(f"Opening {app}.")
            webbrowser.open(sites[app])
        else:
            response = open_any_app(app)
            speak(response if response else f"Attempting to open {app}.")
        return

    # ── SEARCH / PLAY ─────────────────────────────
    if "play" in cmd:
        song = extract_after(cmd, "play")
        if song:
            speak(f"Playing {song} on YouTube.")
            if PYWHATKIT_AVAILABLE:
                pywhatkit.playonyt(song)
            else:
                webbrowser.open(f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}")
        return

    if any(k in cmd for k in ["search for", "look up", "find info", "wikipedia"]):
        topic = re.sub(r"search for|look up|find info|wikipedia|search", "", cmd).strip()
        if topic:
            speak(f"Searching for {topic}.")
            try:
                result = wikipedia.summary(topic, sentences=2, auto_suggest=True)
                speak(result)
            except:
                # Fall back to the local AI.
                reply = ask_ai(f"Give me a brief 2-sentence summary about: {topic}")
                speak(reply)
        return

    # ── VISION ────────────────────────────────────
    if any(k in cmd for k in ["what do you see", "look around", "scan the room", "detect objects", "what is in front"]):
        detect_objects()
        return

    if "open camera" in cmd or "camera on" in cmd:
        speak("Opening camera feed.")
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                cv2.putText(frame, "ROXIE CAMERA | Press ESC to exit",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 230, 255), 2)
                cv2.imshow("Roxie Camera", frame)
            if cv2.waitKey(1) == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
        speak("Camera closed.")
        return

    # ── WIFI / NETWORK ────────────────────────────
    if "wifi on" in cmd or "enable wifi" in cmd:
        speak(wifi_on())
        return
    if "wifi off" in cmd or "disable wifi" in cmd:
        speak(wifi_off())
        return

    # ── FILE SEARCH ───────────────────────────────
    if m := re.search(r"(?:search|find) (?:file|folder) (.+)", cmd):
        name = m.group(1)
        speak(f"Searching for {name}.")
        results = search_laptop(name)
        if results and results[0] != "No files found":
            speak(f"Found {len(results)} result(s).")
            for r in results[:5]:
                print(f"  → {r}")
        else:
            speak("No files matching that name were found.")
        return

    # ── CONVERSATION HISTORY ───────────────────────
    if "clear history" in cmd or "reset conversation" in cmd:
        conversation_history.clear()
        speak(f"Conversation memory cleared, {OWNER_NAME}. Starting fresh.")
        return

    # ── EXIT ──────────────────────────────────────
    if any(k in cmd for k in ["exit", "shutdown roxie", "goodbye", "quit"]):
        farewell = ask_ai(f"Say a brief, witty goodbye to {OWNER_NAME} as Roxie would.")
        speak(farewell)
        sys.exit(0)

    # Local AI fallback
    reply = ask_ai(raw)
    speak(reply)
    log_interaction(raw, reply)

# ══════════════════════════════════════════════════
#  RECOGNIZER
# ══════════════════════════════════════════════════

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8

def get_microphone():
    if not PYAUDIO_AVAILABLE:
        log_status("VOICE", "Microphone disabled: PyAudio is not installed. Typed mode is active.")
        return None
    try:
        names = sr.Microphone.list_microphone_names()
        if not names:
            log_status("VOICE", "No microphone detected.")
            return None
        log_status("VOICE", f"Microphone detected: {names[0]}")
        return sr.Microphone()
    except Exception as e:
        log_status("VOICE", f"Microphone unavailable: {e}")
        return None


mic = get_microphone()


def retry_microphone() -> str:
    """Re-detect the microphone after startup or after a device failure."""
    global mic
    if not PYAUDIO_AVAILABLE:
        return "Microphone support needs PyAudio. Install it with: pip install PyAudio"
    mic = get_microphone()
    if mic is None:
        return "Microphone is still offline. Check Windows microphone permission and PyAudio."
    calibrate_mic()
    return "Microphone reconnected."

def calibrate_mic() -> None:
    if mic is None:
        log_status("VOICE", "Skipping calibration because no microphone is available.")
        return
    log_status("VOICE", "Calibrating microphone...")
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=1.5)
        log_status("VOICE", f"Calibration complete. Energy threshold: {recognizer.energy_threshold:.0f}")
    except Exception as e:
        log_status("VOICE", f"Calibration failed: {e}")

def listen_once(timeout: int = 6, phrase_limit: int = 8) -> str | None:
    global mic
    if mic is None:
        time.sleep(1)
        return None
    try:
        with mic as source:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
        text = recognizer.recognize_google(audio).lower()
        log_status("VOICE", f"Heard: {text}")
        return text
    except sr.WaitTimeoutError:
        log_status("VOICE", "Listening timed out.")
        return None
    except sr.UnknownValueError:
        log_status("VOICE", "Speech was unclear.")
        return None
    except sr.RequestError as e:
        log_status("VOICE", f"Speech recognition service error: {e}")
        return None
    except OSError as e:
        log_status("VOICE", f"Microphone error: {e}")
        mic = None
        return None
    except Exception as e:
        log_status("VOICE", f"Unexpected listening error: {e}")
        return None

# ══════════════════════════════════════════════════
#  STARTUP BANNER
# ══════════════════════════════════════════════════

def print_banner() -> None:
    print("""
========================================
  ROXIE - Iron Edition
  Local AI Assistant powered by Ollama
========================================
""")
    return
    banner = r"""
  ╔══════════════════════════════════════════════════════════╗
  ║                                                          ║
  ║      ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗           ║
  ║      ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝           ║
  ║      ██║███████║██████╔╝██║   ██║██║███████╗           ║
  ║ ██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║           ║
  ║ ╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║           ║
  ║  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝           ║
  ║                                                          ║
  ║       Just A Rather Very Intelligent System              ║
  ║       Powered by Ollama AI  ·  Iron Edition              ║
  ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)

# ══════════════════════════════════════════════════
#  MAIN LOOP
# ══════════════════════════════════════════════════

class RoxieDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def _send_json(self, data, status=200):
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length).decode("utf-8")
            data = json.loads(body or "{}")

            if self.path == "/api/settings":
                for key in ["owner_name", "voice_rate", "voice_index", "ai_model", "max_ai_tokens"]:
                    if key in data:
                        CONFIG[key] = data[key]
                save_config(CONFIG)
                self._send_json({"reply": "Settings saved.", "config": CONFIG})
                return

            if self.path == "/api/command":
                command = str(data.get("command", "")).strip()
                if not command:
                    reply = "No command received."
                else:
                    route_command(command)
                    reply = LAST_RESPONSE or "Command complete."
                self._send_json({"reply": reply})
                return

            self.send_error(404, "Not found")
        except Exception as e:
            self._send_json({"reply": f"Dashboard request failed: {str(e)[:80]}"}, status=500)

    def do_GET(self):
        if self.path == "/api/status":
            self._send_json({
                "assistant": ASSISTANT_NAME,
                "last_response": LAST_RESPONSE,
                "health": health_check(),
                "config": CONFIG,
            })
            return

        if self.path == "/api/logs":
            logs = []
            if os.path.exists(LOG_FILE):
                try:
                    with open(LOG_FILE) as f:
                        logs = json.load(f)
                except Exception:
                    logs = []

            errors = []
            if os.path.exists(ERROR_LOG_FILE):
                try:
                    with open(ERROR_LOG_FILE) as f:
                        errors = json.load(f)
                except Exception:
                    errors = []

            self._send_json({"logs": logs[-50:], "errors": errors[-50:]})
            return

        if self.path == "/api/settings":
            self._send_json(CONFIG)
            return

        if self.path.startswith("/api/files"):
            self._send_json({"reply": file_manager("list files")})
            return

        super().do_GET()


def start_dashboard() -> str | None:
    """Start Roxie's dashboard server and open it in the default browser."""
    global _dashboard_server, _dashboard_thread

    if _dashboard_server:
        return None

    dashboard_dir = Path(__file__).resolve().parent
    dashboard_file = dashboard_dir / "roxie_hud.html"
    if not dashboard_file.exists():
        log_status("SYSTEM", "Dashboard file roxie_hud.html was not found.")
        return None

    handler = functools.partial(RoxieDashboardHandler, directory=str(dashboard_dir))

    for port in range(8000, 8011):
        try:
            socketserver.TCPServer.allow_reuse_address = True
            _dashboard_server = socketserver.TCPServer(("127.0.0.1", port), handler)
            break
        except OSError:
            _dashboard_server = None

    if not _dashboard_server:
        log_status("SYSTEM", "Dashboard server could not start on ports 8000-8010.")
        return None

    _dashboard_thread = threading.Thread(
        target=_dashboard_server.serve_forever,
        daemon=True,
        name="RoxieDashboard",
    )
    _dashboard_thread.start()

    url = f"http://localhost:{_dashboard_server.server_address[1]}/roxie_hud.html"
    webbrowser.open(url)
    log_status("SYSTEM", f"Dashboard opened: {url}")
    return url


def main() -> None:
    print_banner()
    log_status("SYSTEM", "Roxie boot sequence started.")
    log_status("AI", f"Ollama endpoint: {OLLAMA_URL} | model: {CONFIG.get('ai_model', OLLAMA_MODEL)}")
    log_status("VISION", "YOLOv3 vision module available when model files are present.")
    start_dashboard()
    restore_alarms()
    calibrate_mic()

    greeting = ask_ai(
        f"Greet {OWNER_NAME} as Roxie, it's {datetime.datetime.now().strftime('%H:%M')} on "
        f"{datetime.datetime.now().strftime('%A')}. Be warm but professional. One sentence.",
        use_history=False
    )
    speak(greeting)
    speak(f"Say 'Roxie' followed by your command, {OWNER_NAME}. I'm always listening.")
    wait_for_speech()

    log_status("VOICE", "Listening for wake word: Roxie")

    while True:
        try:
            wait_for_speech()
            if mic is None:
                if PYAUDIO_AVAILABLE:
                    retry_microphone()
            if mic is None:
                if PYAUDIO_AVAILABLE:
                    prompt = "[VOICE] Microphone offline. Type a command for Roxie (or type 'retry microphone'): "
                else:
                    prompt = "[VOICE] Typed mode active. Install PyAudio for microphone. Command: "
                text = input(prompt).strip().lower()
            else:
                text = listen_once(timeout=10, phrase_limit=10)
            if not text:
                continue

            text = normalize_wake(text)
            log_status("SYSTEM", f"You said: {text}")

            # Must contain wake word
            if WAKE_TOKEN not in text and mic is not None:
                if any(hint in text for hint in DIRECT_COMMAND_HINTS):
                    route_command(text)
                    continue
                log_status("VOICE", "Wake word not detected.")
                continue

            # Strip wake word to get command
            command = text.replace(WAKE_TOKEN, "").strip() if WAKE_TOKEN in text else text
            if not command:
                speak(f"Yes, {OWNER_NAME}?")
                wait_for_speech()
                # Listen for the actual command
                if mic is None:
                    command_text = input("[VOICE] Command: ").strip().lower()
                else:
                    command_text = listen_once(timeout=8, phrase_limit=10)
                if command_text:
                    command = command_text
                else:
                    continue

            route_command(command)

        except KeyboardInterrupt:
            speak(f"Signing off. Have a productive day, {OWNER_NAME}.")
            break
        except Exception as e:
            log_status("SYSTEM", f"Runtime error: {e}")
            continue

if __name__ == "__main__":
    main()
