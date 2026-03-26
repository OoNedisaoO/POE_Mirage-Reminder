# PoE Mirage Checker Overlay

A lightweight, always-on-top overlay for Path of Exile designed to completely cure "map blindness." 

If you are running hundreds of maps and everything is turning into a blur, it is incredibly easy to autopilot right past the league mechanic. I built this tool to outsource my working memory—it reads your game logs in real-time and tells you if the **Mirage** league mechanic (Verashta, the Afarud Necromancer) has spawned in your current map so you don't have to think about it.

## ✨ Features

* **Visual Indicator:** A simple UI button that sits on top of your game, staying Orange when searching and turning Green when the Mirage is found.
* **Audio Warning:** If you portal to a town or hideout and haven't encountered the Mirage yet, it plays a distinct beep warning you that you missed it.
* **Smart Death Detection:** The tool checks your last 10 log lines for death messages ("has been slain"); if you just died, it suppresses the audio warning so it doesn't annoy you while you recover.
* **State Recovery:** If you accidentally close the tool and restart it, it reads the last 1MB of your log file to instantly remember what map you are in and whether the Mirage had already spawned.
* **Smart Map Tracking:** It tracks zone generation seeds to reset automatically on new maps, while preserving your state if you simply portal to town and re-enter.
* **100% TOS Safe:** This tool does **not** read game memory. It strictly tails your local `Client.txt` log file.
* **Customizable UI:** Click and drag to move, drag the bottom-right corner to resize, or hold `Ctrl + Mouse Wheel` to scale the entire UI (fonts and all) up or down.

## ⚙️ How It Works

Path of Exile writes NPC spawns and dialogue directly to your `Client.txt` file the moment they render in the zone. This script runs a background thread that constantly tails this log file, scanning for the Mirage NPC ("Verashta"). When the keyword is found, it instantly flips the overlay to Green—often before you even walk up to the mechanic!

## 🚀 Installation & Usage

### Prerequisites
1. **Python 3.8 or higher**: Download and install from [python.org](https://www.python.org/downloads/).
2. **Crucial step:** During installation, ensure you check the box that says **"Add Python to PATH"**.

### Dependencies
The app uses only standard Python libraries. **No external `pip install` commands are required.**

### Setup & Running
1. Download the `mirage_checker.py` script.
2. Place it in a dedicated folder (e.g., `C:\POE Tools\Mirage Checker\`).
3. Open PowerShell or CMD and run:
   ```cmd
   cd "C:\POE Tools\Mirage Checker"
   python mirage_checker.py


### 🔧 Troubleshooting
The overlay doesn't turn green? The app automatically looks for your Client.txt in the standard Steam and Standalone install folders. If it can't find it, a text box will appear in the overlay—just paste the full path to your Client.txt and click OK.

Did GGG change the NPC name? If a future patch alters the NPC name, you can open mirage_checker.py in any text editor and update the keywords at the top of the file.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
