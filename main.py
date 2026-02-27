import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from processor import process_xml
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # for PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

selected_file = None


def select_file():
    global selected_file
    selected_file = filedialog.askopenfilename(
        title="Select Spiideo XML File",
        filetypes=[("XML Files", "*.xml")]
    )
    if selected_file:
        status_var.set("File selected.")


def generate_full():
    if not selected_file:
        messagebox.showerror("Error", "Select a file first.")
        return

    output = process_xml(selected_file)
    messagebox.showinfo("Success", f"Created:\n{output}")

def time_to_seconds(time_str):
    try:
        parts = time_str.strip().split(":")

        if len(parts) != 3:
            raise ValueError

        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])

        if hours < 0 or minutes < 0 or seconds < 0:
            raise ValueError

        if minutes >= 60 or seconds >= 60:
            raise ValueError

        if hours > 5:
            raise ValueError

        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds

    except:
        raise ValueError("Time must be in HH:MM:SS format (0–5 hours).")


def show_timestamp_inputs():
    timestamp_frame.pack(pady=20)


def generate_timestamped():
    if not selected_file:
        messagebox.showerror("Error", "Select a file first.")
        return

    try:
        start_seconds = time_to_seconds(start_entry.get())
        end_seconds = time_to_seconds(end_entry.get())

        if start_seconds > end_seconds:
            raise Exception("Start time must be before end time.")

        output = process_xml(selected_file, start_seconds, end_seconds)
        messagebox.showinfo("Success", f"Created:\n{output}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# -------------------------
# GUI
# -------------------------

root = tk.Tk()
root.title("Spiideo Stats Exporter")
root.geometry("1024x768")

main_frame = ttk.Frame(root, padding=30)
main_frame.pack(expand=True)

# -------------------------
# LOGO
# -------------------------

logo_photo = tk.PhotoImage(file=resource_path("vanderbitl_logo.png"))

# Resize (adjust numbers as needed)
logo_photo = logo_photo.subsample(6, 6)

logo_label = ttk.Label(main_frame, image=logo_photo)
logo_label.image = logo_photo
logo_label.pack(pady=(0, 20))

title = ttk.Label(main_frame, text="Vanderbilt Women's Soccer Excel Converter", font=("Segoe UI", 20, "bold"))
title.pack(pady=20)

ttk.Button(main_frame, text="Select XML File", command=select_file).pack(pady=10)

ttk.Button(main_frame, text="Generate Spreadsheet", command=generate_full).pack(pady=10)

ttk.Button(main_frame, text="Generate With Timestamps", command=show_timestamp_inputs).pack(pady=10)

# Timestamp Frame (hidden initially)
timestamp_frame = ttk.Frame(main_frame)

ttk.Label(timestamp_frame, text="Start Time (HH:MM:SS, max 5:00:00):").pack()
start_entry = ttk.Entry(timestamp_frame)
start_entry.pack()

ttk.Label(timestamp_frame, text="End Time (HH:MM:SS, max 5:00:00):").pack()
end_entry = ttk.Entry(timestamp_frame)
end_entry.pack()

ttk.Button(timestamp_frame, text="Generate", command=generate_timestamped).pack(pady=10)

status_var = tk.StringVar()
status_var.set("Ready")

ttk.Label(main_frame, textvariable=status_var).pack(pady=20)

# -------------------------
# Bottom Right Credit
# -------------------------

credit_label = ttk.Label(
    root,
    text="Courtesy of: Raja Swaminathan",
    font=("Segoe UI", 9)
)

credit_label.place(
    relx=1.0,
    rely=1.0,
    anchor="se",
    x=-10,
    y=-10
)

root.mainloop()