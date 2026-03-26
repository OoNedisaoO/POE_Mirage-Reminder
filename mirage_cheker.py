"""
mirage_checker.py — POE Mirage Checker Overlay
================================================
Reads Client.txt in real time (same Traxile-style logic as the POE SSF Logger).

Map detection (new vs portal re-entry):
  • "Generating level N area "X" with seed S" — a new instance is being created.
    If seed S differs from the last seen seed → new map → reset indicator.
    Same seed → portal re-entry → no reset.
  • "You have entered X" followed after a new-instance generation → map confirmed.

Mirage detection:
  • Any log line containing "Verashta" (the Afarud Necromancer NPC) → triggered.
    This fires as soon as the game writes the NPC's spawn / dialogue line,
    meaning the mechanic has appeared on the map — even if you never enter the portal.

Button colours:
  🟢 Green  — Mirage mechanic has spawned on this map.
  🟠 Orange — No Mirage yet on this map (or a new map just started).
"""

import os
import re
import sys
import threading
import time
import tkinter as tk
from pathlib import Path
import tkinter.font as tkfont

# ─── Client.txt search paths (same list as POE SSF Logger) ───────────────────

CLIENT_TXT_PATHS = [
    Path("C:/Program Files (x86)/Grinding Gear Games/Path of Exile/logs/Client.txt"),
    Path("C:/Program Files (x86)/Steam/steamapps/common/Path of Exile/logs/Client.txt"),
    Path("C:/Program Files/Steam/steamapps/common/Path of Exile/logs/Client.txt"),
    Path("C:/Steam/steamapps/common/Path of Exile/logs/Client.txt"),
    Path("D:/Steam/steamapps/common/Path of Exile/logs/Client.txt"),
    Path("D:/SteamLibrary/steamapps/common/Path of Exile/logs/Client.txt"),
    Path("E:/SteamLibrary/steamapps/common/Path of Exile/logs/Client.txt"),
]

# ─── Regex (from TraXile / POE SSF Logger) ───────────────────────────────────

GENERATING_RE = re.compile(r'Generating level (\d+) area "(.+?)" with seed (\d+)')
ENTERED_RE    = re.compile(r"You have entered (.+)\.")

# Areas that are NOT real map runs
HIDEOUT_KEYWORDS = ("hideout", "menagerie", "mine", "sanctuary", "kingsmarch")
TOWN_AREAS = {
    "Lioneye's Watch", "The Forest Encampment", "The Sarn Encampment",
    "Highgate", "Overseer's Tower", "The Bridge Encampment",
    "Oriath Docks", "Oriath", "Karui Shores", "Ogham", "Vastiri",
    "Hideout", "Guild Hideout",
}

# ─── Colours & layout ────────────────────────────────────────────────────────

CLR_BG          = "#0d1117"
CLR_CARD        = "#161b22"
CLR_TEXT        = "#e6edf3"
CLR_DIM         = "#7d8590"
CLR_ORANGE      = "#ff8c00"   # not encountered
CLR_GREEN       = "#2ecc71"   # encountered
CLR_ORANGE_DRK  = "#b36200"
CLR_GREEN_DRK   = "#1e8449"
CLR_TITLE       = "#ffd700"

WINDOW_W = 200
WINDOW_H = 110
MIN_W = 120
MIN_H = 80


# ─── Helpers ─────────────────────────────────────────────────────────────────

def find_client_txt() -> Path | None:
    for p in CLIENT_TXT_PATHS:
        if p.exists():
            return p
    return None


def is_town_or_hideout(name: str) -> bool:
    low = name.lower()
    for kw in HIDEOUT_KEYWORDS:
        if kw in low:
            return True
    return name in TOWN_AREAS


# NPC name keywords — any line in Client.txt that contains one of these
# (case-insensitive) will trigger the indicator.
MIRAGE_NPC_KEYWORDS = (
    "varashta",  # e.g. "Varashta, the Winter Sekhema"
)

def is_mirage_npc_line(line: str) -> bool:
    """True if the log line contains any known Mirage NPC name."""
    low = line.lower()
    return any(kw in low for kw in MIRAGE_NPC_KEYWORDS)


# ─── Log Tailer ──────────────────────────────────────────────────────────────

class MirageLogMonitor:
    """
    Background thread that tails Client.txt.

    Callbacks:
      on_new_map(area_name)  — fired when a genuinely new map seed is detected
      on_mirage()            — fired when a Mirage NPC name appears in the log
    """

    def __init__(self, filepath: Path, on_new_map, on_mirage):
        self.filepath   = filepath
        self.on_new_map = on_new_map
        self.on_mirage  = on_mirage

        self._last_seed            = None
        self._new_instance_pending = False
        self._pending_area         = None
        self._running              = False
        self._thread               = None

    def start(self):
        self._running = True
        self._thread  = threading.Thread(target=self._tail, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def _tail(self):
        with open(self.filepath, "r", encoding="utf-8", errors="replace") as f:
            f.seek(0, os.SEEK_END)   # only watch NEW lines
            while self._running:
                pos  = f.tell()
                line = f.readline()
                if not line:
                    time.sleep(0.25)
                    f.seek(pos)      # Windows file-handle re-sync
                    continue

                # ── Step 1: Mirage NPC detection (highest priority) ──
                # Check EVERY line for the NPC name; this fires as soon as
                # the game logs the NPC's spawn / dialogue.
                if is_mirage_npc_line(line):
                    self.on_mirage()
                    continue

                # ── Step 2: detect new area instance generation ──
                gm = GENERATING_RE.search(line)
                if gm:
                    seed = gm.group(3)
                    area = gm.group(2).strip()
                    if seed != self._last_seed:
                        self._last_seed            = seed
                        self._new_instance_pending = True
                        self._pending_area         = area
                    # Same seed → portal re-entry → don't reset
                    continue

                # ── Step 3: detect zone entry (confirm new map) ──
                em = ENTERED_RE.search(line)
                if em:
                    area_name = em.group(1).strip()

                    # Skip towns / hideouts
                    if is_town_or_hideout(area_name):
                        self._new_instance_pending = False
                        continue

                    # New real map confirmed
                    if self._new_instance_pending:
                        self._new_instance_pending = False
                        self.on_new_map(area_name)


# ─── GUI ─────────────────────────────────────────────────────────────────────

class MirageCheckerApp(tk.Tk):

    def __init__(self, client_txt: Path | None):
        super().__init__()

        self._mirage_found  = False
        self._current_map   = "Waiting for map…"
        self._monitor       = None
        self._client_txt    = client_txt
        self._scale         = 1.0  # Dynamic scaling factor (1.0 = default)

        self._build_ui()
        self._apply_state()

        if client_txt:
            self._start_monitor(client_txt)
        else:
            self._map_var.set("⚠ Client.txt not found")
            self._show_path_entry()

    # ── UI construction ──────────────────────────────────────────────────────

    def _build_ui(self):
        self.title("Mirage Checker")
        self.geometry(f"{WINDOW_W}x{WINDOW_H}+100+100")
        self.resizable(False, False)
        self.configure(bg=CLR_BG)
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.93)

        # Allow dragging
        self.bind("<ButtonPress-1>",   self._drag_start)
        self.bind("<B1-Motion>",       self._drag_motion)
        self.bind("<Control-MouseWheel>", self._on_scale_wheel)
        self.overrideredirect(True)    # frameless window

        # ── Close + drag handle bar ──
        self._bar = tk.Frame(self, bg=CLR_CARD, height=22)
        self._bar.pack(fill="x", side="top")
        self._bar.bind("<ButtonPress-1>", self._drag_start)
        self._bar.bind("<B1-Motion>",     self._drag_motion)

        self._title_lbl = tk.Label(self._bar, text="  ✦ Mirage Checker", bg=CLR_CARD,
                                   fg=CLR_TITLE, font=("Segoe UI", 9, "bold"))
        self._title_lbl.pack(side="left")
        
        self._close_btn = tk.Button(self._bar, text="✕", bg=CLR_CARD, fg=CLR_DIM,
                                    relief="flat", bd=0, font=("Segoe UI", 9),
                                    activebackground="#c0392b", activeforeground="white",
                                    command=self.destroy, cursor="hand2")
        self._close_btn.pack(side="right", padx=4)

        # ── Map label ──
        self._map_var = tk.StringVar(value=self._current_map)
        self._map_lbl = tk.Label(self, textvariable=self._map_var,
                                 bg=CLR_BG, fg=CLR_DIM,
                                 font=("Segoe UI", 8), wraplength=180)
        self._map_lbl.pack(pady=(6, 2))

        # ── Main indicator button ──
        self._btn = tk.Button(
            self, text="NO MIRAGE YET",
            font=("Segoe UI", 10, "bold"),
            relief="flat", bd=0,
            cursor="hand2",
            command=self._manual_toggle,
            width=18, height=2,
        )
        self._btn.pack(pady=4)

        # ── Resize handle ──
        self._grip = tk.Label(self, text="◢", bg=CLR_BG, fg=CLR_DIM,
                              font=("Segoe UI", 8), cursor="size_nw_se")
        self._grip.place(relx=1.0, rely=1.0, anchor="se")
        self._grip.bind("<B1-Motion>", self._resize_motion)
        
        # Initial layout refresh
        self._refresh_layout()

    def _show_path_entry(self):
        """Extra row to let user paste a custom path if auto-detect failed."""
        frame = tk.Frame(self, bg=CLR_BG)
        frame.pack(pady=4, padx=8, fill="x")
        self._path_entry = tk.Entry(frame, bg=CLR_CARD, fg=CLR_TEXT,
                                    insertbackground=CLR_TEXT,
                                    font=("Segoe UI", 7), relief="flat")
        self._path_entry.insert(0, "Paste Client.txt path here…")
        self._path_entry.pack(side="left", fill="x", expand=True, padx=(0, 4))
        tk.Button(frame, text="OK", bg=BTN_BLUE, fg="white",
                  font=("Segoe UI", 7, "bold"), relief="flat",
                  command=self._load_custom_path).pack(side="right")

    # ── Drag & Resize support (frameless window) ──────────────────────────────

    def _drag_start(self, event):
        self._drag_x = event.x_root - self.winfo_x()
        self._drag_y = event.y_root - self.winfo_y()

    def _drag_motion(self, event):
        self.geometry(f"+{event.x_root - self._drag_x}+{event.y_root - self._drag_y}")

    def _resize_motion(self, event):
        new_w = max(MIN_W, event.x_root - self.winfo_rootx())
        new_h = max(MIN_H, event.y_root - self.winfo_rooty())
        
        # Update scale factor based on width relative to default
        self._scale = new_w / WINDOW_W
        self.geometry(f"{new_w}x{new_h}")
        self._refresh_layout()

    def _on_scale_wheel(self, event):
        """Scale with Ctrl + MouseWheel."""
        if event.delta > 0:
            self._scale += 0.05
        else:
            self._scale = max(0.5, self._scale - 0.05)
        
        new_w = int(WINDOW_W * self._scale)
        new_h = int(WINDOW_H * self._scale)
        self.geometry(f"{new_w}x{new_h}")
        self._refresh_layout()

    def _refresh_layout(self):
        """Update fonts and widget sizes based on current self._scale."""
        s = self._scale
        
        # Update Title Bar
        self._bar.config(height=int(22 * s))
        self._title_lbl.config(font=("Segoe UI", int(9 * s), "bold"))
        self._close_btn.config(font=("Segoe UI", int(9 * s)))
        
        # Update Map Label
        self._map_lbl.config(font=("Segoe UI", int(8 * s)), wraplength=int(180 * s))
        
        # Update Main Button
        # width in 'chars', height in 'lines' for tk.Button
        # We also scale the font size
        self._btn.config(
            font=("Segoe UI", int(10 * s), "bold"),
            width=int(18),  # keeping char width constant, font scales it
            height=int(2)
        )
        
        # Update Resize Handle
        self._grip.config(font=("Segoe UI", int(8 * s)))

    # ── State management ─────────────────────────────────────────────────────

    def _apply_state(self):
        if self._mirage_found:
            self._btn.config(
                text="MIRAGE SPAWNED ✓",
                bg=CLR_GREEN, fg="white",
                activebackground=CLR_GREEN_DRK, activeforeground="white"
            )
        else:
            self._btn.config(
                text="NO MIRAGE YET",
                bg=CLR_ORANGE, fg="white",
                activebackground=CLR_ORANGE_DRK, activeforeground="white"
            )

    def _manual_toggle(self):
        """Let the user manually flip the state (in case log misses something)."""
        self._mirage_found = not self._mirage_found
        self._apply_state()

    # ── Monitor callbacks (called from background thread) ────────────────────

    def _on_new_map(self, area_name: str):
        self._mirage_found  = False
        self._current_map   = area_name
        # Schedule UI update on the main thread
        self.after(0, self._refresh_map_ui)

    def _on_mirage(self):
        self._mirage_found = True
        self.after(0, self._apply_state)

    def _refresh_map_ui(self):
        self._map_var.set(f"📍 {self._current_map}")
        self._apply_state()

    # ── Monitor setup ────────────────────────────────────────────────────────

    def _start_monitor(self, path: Path):
        self._monitor = MirageLogMonitor(path, self._on_new_map, self._on_mirage)
        self._monitor.start()

    def _load_custom_path(self):
        raw = self._path_entry.get().strip()
        p   = Path(raw)
        if p.exists():
            self._client_txt = p
            self._start_monitor(p)
        else:
            self._map_var.set("⚠ File not found")

    # ── Cleanup ──────────────────────────────────────────────────────────────

    def destroy(self):
        if self._monitor:
            self._monitor.stop()
        super().destroy()


# ─── Colour constant needed by _show_path_entry ──────────────────────────────

BTN_BLUE = "#3a86ff"

# ─── Entry point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    client = find_client_txt()
    app    = MirageCheckerApp(client)
    app.mainloop()
