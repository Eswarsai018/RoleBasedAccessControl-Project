import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import time

# Create the main application window
root = tk.Tk()
root.title("Clock Application")
root.geometry("1000x800")  # Set the size of the window

# Center the window on the screen
root.eval('tk::PlaceWindow . center')

# Load the background image
bg_image_original = Image.open(r"RBAC_login.png")

# Function to resize and apply the background image
def resize_background(event=None):
    new_width = root.winfo_width()
    new_height = root.winfo_height()
    resized_image = bg_image_original.resize((new_width, new_height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)
    background_label.config(image=bg_image)
    background_label.image = bg_image  # Keep a reference to avoid garbage collection

# Set the background image label to cover the entire window
background_label = tk.Label(root)
background_label.place(relwidth=1, relheight=1)
resize_background()  # Set the initial background
root.bind("<Configure>", resize_background)  # Update background on window resize

# Title label style with custom colors (for professional theme)
title_label = tk.Label(
    root,
    text="Clock Application",
    font=("Helvetica", 24, "bold", "underline"),
    fg="#A7A9B7",  # Light gray color for text (professional)
    bg="#1E2A47",  # Dark blue background (professional)
    padx=20,
    pady=10
)
title_label.pack(fill="x", pady=10)  # Expand horizontally to fill the top of the window

# Create a frame for the clock display
clock_frame = tk.Frame(root, bg="#1E2A47", padx=20, pady=20)
clock_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

# Label style for clock display
clock_label = tk.Label(clock_frame, text="", font=("Helvetica", 48, "bold"), fg="#A7A9B7", bg="#1E2A47")
clock_label.pack()

# Function to update the clock display every second
def update_clock():
    current_time = time.strftime("%H:%M:%S")  # Get the current time in HH:MM:SS format
    clock_label.config(text=current_time)
    clock_label.after(1000, update_clock)  # Update the time every 1000 ms (1 second)

# Start updating the clock
update_clock()

# Start the application
root.mainloop()
