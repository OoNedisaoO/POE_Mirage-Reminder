# 🌌 PoE Mirage Checker Overlay

A lightweight, always-on-top overlay for Path of Exile designed to completely cure "map blindness." 

If you are running hundreds of maps, it is incredibly easy to autopilot right past the league mechanic. This tool reads your game logs in real-time and tells you if the **Mirage** (Verashta, the Afarud Necromancer) has spawned in your current map so you don't have to think about it.

---

## 🚀 Quick Start (Windows EXE)

The easiest way to use the tool without installing Python.

1.  **Download:** Go to the [Releases](https://github.com/OoNedisaoO/Mirage-Helper/releases) page and download `MirageHelper.exe`.
2.  **Run:** Double-click the EXE. 
    * *Note: Windows might show a "SmartScreen" warning because the EXE isn't digitally signed. Click **"More Info"** -> **"Run Anyway"**.*
3.  **Position:** Drag the overlay anywhere on your screen.
4.  **Scaling:** Hold `Ctrl + Mouse Wheel` to scale the UI size (fonts and window) up or down.

---

## ✨ Features

* **Real-time Detection:** Automatically turns **🟢 Green** the second Verashta is detected in the logs.
* **Audio Warning:** Plays a distinct beep if you leave a map (portal to town/hideout) without finding the Mirage.
* **Smart Death Detection:** The tool checks your last 10 log lines for death messages; if you just died, it suppresses the audio warning.
* **State Recovery:** If you restart the tool mid-map, it reads the last 1MB of your log to instantly remember your current map state.
* **100% TOS Safe:** Does **not** read game memory or inject code. It strictly "tails" the local `Client.txt` log file.

---

## 🛠️ Manual Installation (Python)

If you prefer to run the source code directly:

### Prerequisites
* **Python 3.8+** (Ensure "Add Python to PATH" is checked during install).
* The app uses only standard Python libraries (**No `pip install` required**).

### Running
```powershell
python mirage_checker.py
