import tkinter as tk
from tkinter import ttk
import os
import datetime
import sys
import platform

# --- CONFIG ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "data.txt")

# Platform Detection
IS_MAC = platform.system() == "Darwin"
IS_LINUX = platform.system() == "Linux"
IS_WIN = platform.system() == "Windows"

# Sound Command
if IS_MAC:
    SOUND_CMD = "afplay /System/Library/Sounds/Ping.aiff &"
elif IS_LINUX:
    SOUND_CMD = "paplay /usr/share/sounds/freedesktop/stereo/camera-shutter.oga &"
else:
    SOUND_CMD = "echo 'beep'" # Windows fallback

# Apple-Style Theme (Light/Frosted Look)
BG_COLOR = "#F5F5F7"       # Apple Light Grey
FG_COLOR = "#1D1D1F"       # Apple Dark Grey (Text)
ACCENT_COLOR = "#007AFF"   # Apple Blue
SUCCESS_COLOR = "#34C759"  # Apple Green
WARN_COLOR = "#FF9500"     # Apple Orange
FONT_FAMILY = "SF Pro Display" if IS_MAC else "Helvetica Neue"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f: pass

def get_today_count():
    today = datetime.date.today().isoformat()
    count = 0
    try:
        with open(DATA_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2 and parts[0] == today:
                    count = int(parts[1])
    except Exception: pass
    return count

def save_count(count):
    today = datetime.date.today().isoformat()
    lines = []
    found = False
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: lines = f.readlines()
    new_lines = []
    for line in lines:
        parts = line.strip().split(",")
        if len(parts) == 2 and parts[0] == today:
            new_lines.append(f"{today},{count}\n")
            found = True
        else: new_lines.append(line)
    if not found: new_lines.append(f"{today},{count}\n")
    with open(DATA_FILE, "w") as f: f.writelines(new_lines)

def on_click():
    current = count_var.get()
    new_val = current + 1
    count_var.set(new_val)
    save_count(new_val)
    update_ui(new_val)
    os.system(SOUND_CMD)

def update_ui(val):
    if val >= 100:
        status_lbl.config(text="GOAL SMASHED! 🚀", foreground=SUCCESS_COLOR)
        style.configure("TProgressbar", background=SUCCESS_COLOR)
    elif val >= 80:
        status_lbl.config(text="FINISH STRONG! 🔥", foreground=WARN_COLOR)
        style.configure("TProgressbar", background=WARN_COLOR)
    elif val >= 50:
        status_lbl.config(text="HALFWAY THERE.", foreground=ACCENT_COLOR)
        style.configure("TProgressbar", background=ACCENT_COLOR)
    else:
        status_lbl.config(text="PICK UP THE PHONE.", foreground="#86868B")
        style.configure("TProgressbar", background=ACCENT_COLOR)

# --- GUI SETUP ---
root = tk.Tk()
root.title("Project 100")
root.geometry("300x280")
root.attributes("-topmost", True)  # ALWAYS ON TOP
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# Styling
style = ttk.Style()
style.theme_use('clam') # Clean base theme

# Configure Progress Bar Styles
style.configure("TProgressbar", 
    troughcolor="#E5E5EA", 
    background=ACCENT_COLOR, 
    thickness=6, 
    borderwidth=0
)

# Configure Button Style (Rounded simulation via border/padding)
style.configure("TButton", 
    font=(FONT_FAMILY, 14, "bold"), 
    background=ACCENT_COLOR, 
    foreground="white", 
    borderwidth=0, 
    focuscolor="none"
)
style.map("TButton", 
    background=[("active", "#0062CC"), ("pressed", "#004999")], 
    relief=[("pressed", "sunken")]
)

# Header
tk.Label(root, text="PROJECT 100", font=(FONT_FAMILY, 13, "bold"), bg=BG_COLOR, fg="#86868B").pack(pady=(25, 5))

# Count Display
count_var = tk.IntVar(value=get_today_count())
count_lbl = tk.Label(root, textvariable=count_var, font=(FONT_FAMILY, 60, "bold"), bg=BG_COLOR, fg=FG_COLOR)
count_lbl.pack(pady=0)

# Button Wrapper
btn_frame = tk.Frame(root, bg=BG_COLOR, pady=10)
btn_frame.pack()
btn = ttk.Button(btn_frame, text="+1 CALL", command=on_click, width=14)
btn.pack(ipady=10)

# Progress Bar
progress = ttk.Progressbar(root, variable=count_var, maximum=100, length=240, mode='determinate', style='TProgressbar')
progress.pack(pady=15)

# Status Text
status_lbl = tk.Label(root, text="START THE GRIND.", font=(FONT_FAMILY, 11, "italic"), bg=BG_COLOR, fg="#86868B")
status_lbl.pack(pady=(0, 20))

# Initial State
update_ui(count_var.get())

root.mainloop()
