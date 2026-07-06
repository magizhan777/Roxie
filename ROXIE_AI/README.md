# Roxie - Iron Edition

Local beginner-friendly AI assistant powered by Ollama.

## Quick Start

### 1. Start Ollama

```powershell
ollama pull llama3
ollama serve
```

If `ollama serve` says port `11434` is already in use, Ollama is already running.

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run Roxie

```powershell
python roxie.py
```

### 4. Open the dashboard

```powershell
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/roxie_hud.html
```

## Wake Words

Roxie listens for common noisy speech-recognition versions of the name:

```text
roxie, roxy, roxxy, roxey, roxi, roxe, roksy, rocksy,
rocky, rocks, proxy, foxy, rosie, rose, rashi, raksi,
rakhi, ruxi, ruksy, raw see, rock see, hey roxie, ok roxie
```

## Example Commands

| Say | What happens |
|---|---|
| `Roxie, what time is it?` | Tells the current time |
| `Roxie, system status` | CPU, RAM, battery report |
| `Roxie, open YouTube` | Opens YouTube |
| `Roxie, play Bohemian Rhapsody` | Plays on YouTube |
| `Roxie, set volume to 60` | Sets system volume to 60% |
| `Roxie, set brightness to 80` | Sets display brightness |
| `Roxie, take a screenshot` | Captures and saves screen |
| `Roxie, what do you see?` | Activates YOLOv3 vision |
| `Roxie, remember my name is Tony` | Stores in memory |
| `Roxie, what is my name?` | Recalls from memory |
| `Roxie, search for quantum computing` | Wikipedia + Ollama |
| `Roxie, anything else` | Ollama answers locally |

## Files

```text
Roxie_AI/
  roxie.py              Main assistant
  roxie_hud.html        Browser dashboard
  requirements.txt      Python packages
  roxie_memory.json     Auto-created memory
  roxie_log.json        Auto-created interaction log
  roxie_config.json     Auto-created config
```

## Notes

Roxie uses local Ollama at:

```text
http://localhost:11434/api/generate
```

Model:

```text
llama3
```
