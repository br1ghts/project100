import tkinter as tk
from tkinter import ttk
import os
import datetime

# --- CONFIG ---
DATA_FILE = os.path.expanduser("~/Desktop/Project100/data.txt")
SOUND_CMD = "paplay /usr/share/sounds/freedesktop/stereo/camera-shutter.oga &"  # Simple sound on most Linux

# Ensure data file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        pass

def get_today_count():
    today = datetime.date.today().isoformat()
    count = 0
    try:
        with open(DATA_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2 and parts[0] == today:
                    count = int(parts[1])
    except Exception:
        pass
    return count

def save_count(count):
    today = datetime.date.today().isoformat()
    lines = []
    found = False
    
    # Read existing lines
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            lines = f.readlines()
    
    # Update or append
    new_lines = []
    for line in lines:
        parts = line.strip().split(",")
        if len(parts) == 2 and parts[0] == today:
            new_lines.append(f"{today},{count}\n")
            found = True
        else:
            new_lines.append(line)
    
    if not found:
        new_lines.append(f"{today},{count}\n")
        
    with open(DATA_FILE, "w") as f:
        f.writelines(new_lines)

def on_click():
    current = count_var.get()
    new_val = current + 1
    count_var.set(new_val)
    save_count(new_val)
    update_ui(new_val)
    os.system(SOUND_CMD)

def update_ui(val):
    if val >= 100:
        status_lbl.config(text="GOAL SMASHED! 🚀", foreground="green")
        style.configure("TProgressbar", background="green")
    elif val >= 80:
        status_lbl.config(text="FINISH STRONG! 🔥", foreground="orange")
        style.configure("TProgressbar", background="orange")
    elif val >= 50:
        status_lbl.config(text="HALFWAY THERE.", foreground="blue")
        style.configure("TProgressbar", background="blue")
    else:
        status_lbl.config(text="PICK UP THE PHONE.", foreground="black")
        style.configure("TProgressbar", background="grey")

# --- GUI SETUP ---
root = tk.Tk()
root.title("Project 100")
root.geometry("300x250")
root.attributes("-topmost", True)  # Always on top

style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", font=("Helvetica", 14, "bold"))
style.configure("Big.TLabel", font=("Helvetica", 48, "bold"))

# Header
ttk.Label(root, text="PROJECT 100", font=("Helvetica", 16, "bold")).pack(pady=10)

# Count Display
count_var = tk.IntVar(value=get_today_count())
count_lbl = ttk.Label(root, textvariable=count_var, style="Big.TLabel")
count_lbl.pack()

# Button
btn = ttk.Button(root, text="+1 CALL", command=on_click)
btn.pack(pady=10, ipadx=20, ipady=10)

# Progress Bar
progress = ttk.Progressbar(root, variable=count_var, maximum=100, length=250, mode='determinate')
progress.pack(pady=10)

# Status Text
status_lbl = ttk.Label(root, text="START THE GRIND.", font=("Helvetica", 10, "italic"))
status_lbl.pack()

# Initial State
update_ui(count_var.get())

root.mainloop()
