import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
from datetime import datetime

# Create the main application window
root = tk.Tk()
root.title("Date Application")
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
    text="Date Application",
    font=("Helvetica", 24, "bold", "underline"),
    fg="#A7A9B7",  # Light gray color for text (professional)
    bg="#1E2A47",  # Dark blue background (professional)
    padx=20,
    pady=10
)
title_label.pack(fill="x", pady=10)  # Expand horizontally to fill the top of the window

# Create a frame for the date display
date_frame = tk.Frame(root, bg="#1E2A47", padx=20, pady=20)
date_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

# Label style for date display
date_label = tk.Label(date_frame, text="", font=("Helvetica", 48, "bold"), fg="#A7A9B7", bg="#1E2A47")
date_label.pack()

# Function to update the date display every day (just once, as the date changes once per day)
def update_date():
    current_date = datetime.now().strftime("%B %d, %Y")  # Get the current date in 'Month day, year' format
    date_label.config(text=current_date)

# Update the date on startup
update_date()

# Start the application
root.mainloop()
