# 🌌 PoE Mirage Reminder Overlay

A lightweight, always-on-top overlay for Path of Exile designed to completely cure "map blindness." 

If you are running hundreds of maps, it is incredibly easy to autopilot right past the league mechanic. This tool reads your game logs in real-time and tells you if the **Mirage** (Verashta, the Afarud Necromancer) has spawned in your current map so you don't have to think about it.

<img width="250" height="138" alt="image" src="https://github.com/user-attachments/assets/029b8d0a-dca8-4d0a-8f31-c76e49105675" />

<img width="250" height="138" alt="image" src="https://github.com/user-attachments/assets/48e82ff8-774b-49e4-9334-19296915790d" />


---

## 🚀 Quick Start (Windows EXE)

The easiest way to use the tool without installing Python.

1.  **Download:** Go to the [Releases] page and download `MirageReminder.exe`.
2.  **Run:** Double-click the EXE. 
    * *Note: Windows might show a "SmartScreen" warning because the EXE isn't digitally signed. Click **"More Info"** -> **"Run Anyway"**.*
3.  **Position:** Drag the overlay anywhere on your screen.
4.  **Scaling:** Hold `Ctrl + Mouse Wheel` to scale the UI size (fonts and window) up or down.

---

## ✨ Features

* **Real-time Detection:** Automatically turns **🟢 Green** the second Verashta is detected in the logs.
* **Audio Warning:** Plays a distinct beep if you leave a map (portal to town/hideout) without finding the Mirage.
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
python mirage_reminder.py
