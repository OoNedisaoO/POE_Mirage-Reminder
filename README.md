# PoE Mirage Checker Overlay

A lightweight, always-on-top overlay for Path of Exile designed to completely cure "map blindness." 

If you are running hundreds of maps and everything is turning into a blur, it is incredibly easy to autopilot right past the league mechanic. I built this tool to outsource my working memory—it reads your game logs in real-time and tells you if the **Mirage** league mechanic (Verashta, the Afarud Necromancer) has spawned in your current map so you don't have to think about it.

## ✨ Features

* **Visual Indicator:** A simple UI button that sits on top of your game.
  * 🟠 **Orange:** No Mirage yet on this map (or a new map just started).
  * 🟢 **Green:** The Mirage mechanic has spawned on this map!
* **Smart Map Tracking:** It tracks zone generation seeds. It automatically resets to Orange when you start a *new* map instance, but remembers your state if you just portal to town and re-enter the same seed.
* **100% TOS Safe:** This tool does **not** read game memory or interact with the game client. It strictly tails your local `Client.txt` log file, which is fully allowed by Grinding Gear Games.
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

   🔧 Troubleshooting
The overlay doesn't turn green? The app automatically looks for your Client.txt in the standard Steam and Standalone install folders. If it can't find it, a text box will appear in the overlay—just paste the full path to your Client.txt and click OK.

Did GGG change the NPC name? If a future patch alters the NPC name, you can open mirage_checker.py in any text editor and update the keywords at the top of the file.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
