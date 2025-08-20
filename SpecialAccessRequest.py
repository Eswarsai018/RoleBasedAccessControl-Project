import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3  # Use sqlite3 for SQLite database connection

# Create the main application window for Special Access Request page
special_access_root = tk.Tk()
special_access_root.title("Special Access Request")
special_access_root.geometry("800x600")  # Set the size of the window

# Center the window on the screen
special_access_root.eval('tk::PlaceWindow . center')

# Load the background image
bg_image_original = Image.open(r"RBAC_login.png")

# Function to resize and apply the background image
def resize_background(event=None):
    new_width = special_access_root.winfo_width()
    new_height = special_access_root.winfo_height()
    resized_image = bg_image_original.resize((new_width, new_height), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(resized_image)
    background_label.config(image=bg_image)
    background_label.image = bg_image  # Keep a reference to avoid garbage collection

# Set the background image label to cover the entire window
background_label = tk.Label(special_access_root)
background_label.place(relwidth=1, relheight=1)
resize_background()  # Set the initial background
special_access_root.bind("<Configure>", resize_background)  # Update background on window resize

# Title label style with custom colors (professional)
title_label = tk.Label(
    special_access_root,
    text="Special Access Request",
    font=("Helvetica", 24, "bold", "underline"),
    fg="#A7A9B7",  # Light gray color for text (professional)
    bg="#1E2A47",  # Dark blue background (professional)
    padx=20,
    pady=10
)
title_label.pack(fill="x", pady=20)

# Create a frame for the form
form_frame = tk.Frame(special_access_root, bg="#1E2A47", padx=20, pady=20)
form_frame.pack(fill="both", expand=True)

# Special Access Fields
special_access_label = tk.Label(form_frame, text="Special Access Information", font=("Helvetica", 16, "bold"), fg="#A7A9B7", bg="#1E2A47")
special_access_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

# Employee ID
employee_id_label = tk.Label(form_frame, text="Employee ID (6 digits):", font=("Helvetica", 12), fg="#A7A9B7", bg="#1E2A47")
employee_id_label.grid(row=1, column=0, pady=5, sticky="e")
employee_id_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
employee_id_entry.grid(row=1, column=1, pady=5)

# Special Access Application (Dropdown with Data and Clock Application)
special_access_app_label = tk.Label(form_frame, text="Special Access Application:", font=("Helvetica", 12), fg="#A7A9B7", bg="#1E2A47")
special_access_app_label.grid(row=2, column=0, pady=5, sticky="e")
special_access_app_combobox = ttk.Combobox(form_frame, font=("Helvetica", 12), width=27, values=["Date Application", "Clock Application", "Special Access Data", "Log Data"])
special_access_app_combobox.grid(row=2, column=1, pady=5)

# Function to fetch the last EmployeeID from the Log table
def fetch_last_employee_id():
    conn = sqlite3.connect("rbac_group6.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT EmployeeID
        FROM Log
        ORDER BY LogID DESC
        LIMIT 1
    """)
    result1 = cursor.fetchone()

    if result1 is None:
        employee_id_log = 1  # Default to 1 if no log entries found
    else:
        employee_id_log = result1[0]  # Extract the EmployeeID from the result tuple
    
    conn.close()
    return employee_id_log

# Function to populate the Employee ID entry field with the last EmployeeID from the log
def auto_populate_employee_id():
    employee_id_log = fetch_last_employee_id()  # Get the last EmployeeID from the log
    employee_id_entry.insert(0, employee_id_log)  # Auto-populate the Employee ID field

# Call the auto_populate_employee_id function when the form is loaded
auto_populate_employee_id()

# Function to insert special access data into the database
def submit_special_access():
    employee_id = employee_id_entry.get()
    special_access_app = special_access_app_combobox.get()

    # Validate Employee ID (6 digits)
    if len(employee_id) > 6 or not employee_id.isdigit():
        messagebox.showerror("Error", "Employee ID must not be more than 6 digits.")
        return

    # Check if all fields are filled
    if not (employee_id and special_access_app):
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    # Connect to the database
    conn = sqlite3.connect("rbac_group6.db")
    cursor = conn.cursor()

    try:
        # Insert data into SpecialAccess table
        cursor.execute("""
            INSERT INTO SpecialAccess (EmployeeID, SpecialAccessApplication, Approval, IsActive, "CreatedOn", "CreatedBy", "UpdatedOn", "UpdatedBy")
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (employee_id, special_access_app, False, False, sqlite3.datetime.datetime.now(), employee_id, sqlite3.datetime.datetime.now(), employee_id))  # Default Approval and IsActive to False
        conn.commit()

        # Show success message
        messagebox.showinfo("Success", "Special Access Request submitted successfully!")
        cursor.execute("""
            SELECT EmployeeID
            FROM Log
            ORDER BY LogID DESC
            LIMIT 1
            """)
        result1 = cursor.fetchone()

        if result1 is None:
            employee_id = 1 
        else:
            employee_id = result1[0]  # Extract the EmployeeID from the result tuple

        # Create the log message
        log_message = f"Submitted Special Access"

        # Insert the log entry into the Log table
        cursor.execute("""
            INSERT INTO Log (EmployeeID, Action, Timestamp)
            VALUES (?, ?, ?)
            """, (employee_id, log_message, sqlite3.datetime.datetime.now()))
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {e}")
    finally:
        conn.close()  # Close the database connection

    special_access_root.destroy()  # Close the form after submission (optional)

# Submit button
submit_button = tk.Button(form_frame, text="Submit Request", font=("Helvetica", 12), width=20, command=submit_special_access)
submit_button.grid(row=5, column=0, columnspan=2, pady=20)

# Start the application window
special_access_root.mainloop()
