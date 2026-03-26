PoE Mirage Checker Overlay
A lightweight, always-on-top overlay for Path of Exile that completely cures "map blindness."

If you are running hundreds of maps and everything is turning into a blur, it is incredibly easy to autopilot right past the league mechanic. I built this tool to outsource my working memory—it reads your game logs in real-time and tells you if the Mirage league mechanic has spawned in your current map so you don't have to think about it.

✨ Features
Visual Indicator: A simple UI button that sits on top of your game.

🟠 Orange: No Mirage detected yet, or you just entered a fresh map.

🟢 Green: The Mirage mechanic is currently on this map!

Smart Map Tracking: It tracks zone generation seeds. It automatically resets to Orange when you start a new map, but remembers your state if you just portal to town and come back.

100% TOS Safe: This tool does not read game memory or interact with the game client. It strictly tails your local Client.txt log file, which is fully allowed by Grinding Gear Games.

Customizable UI: Click and drag to move, drag the corner to resize, or hold Ctrl + Mouse Wheel to scale the entire UI up or down.

⚙️ How It Works
Path of Exile writes NPC spawns and dialogue directly to your Client.txt file the moment they render in the zone. This script runs a background thread that constantly tails this log file, scanning for the Mirage NPC ("Varashta"). When the keyword is found, it instantly flips the overlay to Green—often before you even walk up to the mechanic!

🚀 Installation & Usage
Prerequisites
Python 3.8 or higher: Download from python.org.

Crucial step: During installation, ensure you check the box that says "Add Python to PATH".

Setup
Download the mirage_checker.py script.

Place it in a dedicated folder (e.g., C:\POE Tools\Mirage Checker\).

The app uses only standard Python libraries, so no extra pip install commands are required!

Running the Tool
You can run the script via your command line:

DOS
cd "C:\POE Tools\Mirage Checker"
python mirage_checker.py
(Tip: You can also easily add this to a batch .bat file alongside Awakened PoE Trade to launch everything at once!)

🔧 Troubleshooting
The overlay doesn't turn green? The app automatically looks for your Client.txt in the standard Steam and Standalone install folders. If your game is installed elsewhere, the UI will prompt you to paste the correct file path.

Did GGG change the NPC name? If a future patch alters the NPC name, you can easily open mirage_checker.py in any text editor and update the keyword list at the top of the file.
