import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry  # Import DateEntry for date picker
import sqlite3
import os  # To navigate between scripts

# Create the main application window
root = tk.Tk()
root.title("Create Employee")
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

# Title label style with custom colors (for hedge fund)
title_label = tk.Label(
    root,
    text="Create New Employee",
    font=("Helvetica", 24, "bold", "underline"),
    fg="#A7A9B7",  # Light gray color for text (professional)
    bg="#1E2A47",  # Dark blue background (professional)
    padx=20,
    pady=10
)
title_label.pack(fill="x", pady=10)  # Expand horizontally to fill the top of the window

# Create a frame for the sign-up fields to center them
signup_frame = tk.Frame(root, bg="#1E2A47", padx=20, pady=20)
signup_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

# Function to handle placeholder text
def add_placeholder(entry, placeholder):
    """Adds placeholder text to an entry widget."""
    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)  # Clear the placeholder when focus is on the entry
            entry.config(fg="black")
    
    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)  # Re-add placeholder when focus leaves and nothing is entered
            entry.config(fg="gray")  # Change text color to gray to indicate placeholder
    
    entry.insert(0, placeholder)
    entry.config(fg="gray")  # Set initial text color to gray (indicating placeholder)
    
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# Fancy Label style with dark blue background (professional theme)
label_style = {
    "font": ("Helvetica", 12, "bold"),
    "bg": "#1E2A47",  # Dark blue background color
    "fg": "#A7A9B7",  # Light gray text for contrast
    "padx": 15,
    "pady": 10,
    "relief": "solid",  # Adds a solid border for a fancy look
    "bd": 2,
    "highlightthickness": 0
}

# Function to validate phone input
def validate_phone_input(P):
    return len(P) <= 10 and (P.isdigit() or P == "")

# Function to validate RoleID and ManagerID
def validate_id_input(P):
    return len(P) <= 6 and (P.isdigit() or P == "")

# Function to validate Department input length
def validate_department_length(P):
    return len(P) <= 50

def validate_name_length(P):
    return len(P) <= 50

# Validation registrations
phone_validate = root.register(validate_phone_input)
id_validate = root.register(validate_id_input)
department_validate = root.register(validate_department_length)
name_validate = root.register(validate_name_length)

# Row 1 - EmployeeID (auto-generated, hidden field) and Email
employee_id_label = tk.Label(signup_frame, text="Employee ID (auto-generated):", **label_style)
employee_id_label.grid(row=0, column=0, padx=10, pady=15, sticky="e")
employee_id_entry = tk.Entry(signup_frame, font=("Helvetica", 12), width=25, state="disabled", highlightthickness=0)
employee_id_entry.grid(row=0, column=1, padx=10, pady=15)

email_label = tk.Label(signup_frame, text="Email:", **label_style)
email_label.grid(row=0, column=2, padx=10, pady=15, sticky="e")
email_entry = tk.Entry(signup_frame, font=("Helvetica", 12), width=25, highlightthickness=0)
email_entry.grid(row=0, column=3, padx=10, pady=15)

# Other fields
fields = {
    "First Name": {"row": 1, "column": 0},
    "Last Name": {"row": 1, "column": 2},
    "Password": {"row": 2, "column": 0},
    "Phone": {"row": 2, "column": 2},
    "Department": {"row": 3, "column": 0},
    "Role ID": {"row": 3, "column": 2},
    "Manager ID": {"row": 4, "column": 0},
    "Hire Date": {"row": 4, "column": 2}
}

entries = {}
for field, config in fields.items():
    label = tk.Label(signup_frame, text=f"{field}:", **label_style)
    label.grid(row=config["row"], column=config["column"], padx=10, pady=15, sticky="e")
    
    entry = tk.Entry(signup_frame, font=("Helvetica", 12), width=25, highlightthickness=0)
    if field == "Phone":
        entry.config(validate="key", validatecommand=(phone_validate, "%P"))
    elif field in ["Role ID", "Manager ID"]:
        entry.config(validate="key", validatecommand=(id_validate, "%P"))
    elif field == "Department":
        entry.config(validate="key", validatecommand=(department_validate, "%P"))
    elif field in ["First Name", "Last Name"]:
        entry.config(validate="key", validatecommand=(name_validate, "%P"))
    elif field == "Hire Date":
        entry = DateEntry(signup_frame, font=("Helvetica", 12), width=23)
    
    entry.grid(row=config["row"], column=config["column"] + 1, padx=10, pady=15)
    entries[field] = entry

# Function to go back
def go_back():
    root.destroy()
    os.system("python mainpage.py")

# Back Button
back_button = tk.Button(
    root,
    text="Back",
    font=("Helvetica", 12, "bold"),
    bg="#A7A9B7",
    fg="#1E2A47",
    command=go_back
)
back_button.place(relx=0.95, rely=0.05, anchor="ne")

# Function to handle form submission
def submit_form():
    email = email_entry.get()
    first_name = entries["First Name"].get()
    last_name = entries["Last Name"].get()
    password = entries["Password"].get()
    phone = entries["Phone"].get()
    department = entries["Department"].get()
    role_id = entries["Role ID"].get()
    manager_id = entries["Manager ID"].get()
    hire_date = entries["Hire Date"].get()
    
    if not email or not password or not phone or not department or not first_name or not last_name or not role_id or not hire_date:
        messagebox.showwarning("Validation Error", "All fields are required.")
        return
    
    try:
        conn = sqlite3.connect("rbac_group6.db")  # Replace with your database path
        cursor = conn.cursor()
        
        # Check for duplicate email
        cursor.execute("SELECT COUNT(*) FROM Employee WHERE Email = ?", (email,))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Duplicate Data", "Duplicate data - Email ID is already present.")
            return
        
        cursor.execute("SELECT COUNT(*) FROM Employee WHERE EmployeeID = ? AND RoleID <= 2", (manager_id,))
        if cursor.fetchone()[0] == 0:
            messagebox.showerror("Invalid Manager", "The entered Manager ID is invalid or does not have the Manager role.")
            return
        
        # Insert data into the database
        cursor.execute("""
            INSERT INTO Employee (FirstName, LastName, Email, Password, Phone, Department, RoleID, HireDate, ManagerID, IsActive, CreatedOn, CreatedBy, UpdatedOn, UpdatedBy)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, email, password, phone, department, role_id, hire_date, manager_id, 1, sqlite3.datetime.datetime.now(), 1, sqlite3.datetime.datetime.now(), 1))
        
        
        conn.commit()
        messagebox.showinfo("Success", "Employee created successfully.")
        
        # Get the most recent EmployeeID from the Log table
        cursor.execute("""
            SELECT EmployeeID
            FROM Log
            ORDER BY LogID DESC
            LIMIT 1
            """)
        result1 = cursor.fetchone()

        # If there is no result (i.e., the Log table is empty), set a default EmployeeID
        if result1 is None:
            employee_id = 1  # Assuming 1 is the default ID for the first employee (or handle accordingly)
        else:
            employee_id = result1[0]  # Extract the EmployeeID from the result tuple

        # Create the log message
        log_message = f"Created a new employee - {first_name} {last_name}"

        # Insert the log entry into the Log table
        cursor.execute("""
            INSERT INTO Log (EmployeeID, Action, Timestamp)
            VALUES (?, ?, ?)
            """, (employee_id, log_message, sqlite3.datetime.datetime.now()))

        # Commit the changes to the database
        conn.commit()

        email_entry.delete(0, tk.END)
        for field in entries.values():
            field.delete(0, tk.END)
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

# Submit Button
submit_button = tk.Button(
    signup_frame,
    text="Submit",
    font=("Helvetica", 14, "bold"),
    bg="#A7A9B7",
    fg="#1E2A47",
    command=submit_form
)
submit_button.grid(row=5, column=1, pady=20)

# Function to generate the next Employee ID
def generate_employee_id():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("rbac_group6.db")  # Replace with your actual database name
        cursor = conn.cursor()

        # Query to get the maximum EmployeeID from the Employee table
        cursor.execute("SELECT MAX(EmployeeID) FROM Employee")
        result = cursor.fetchone()

        # Generate the next Employee ID
        if result[0] is None:
            new_employee_id = 1  # If no employees exist, start with 1
        else:
            new_employee_id = result[0] + 1  # Increment the highest EmployeeID by 1

        # Set the new Employee ID in the entry field
        employee_id_entry.config(state="normal")  # Enable the text entry to modify it
        employee_id_entry.delete(0, tk.END)  # Clear the current value
        employee_id_entry.insert(0, str(new_employee_id))  # Insert the new Employee ID
        employee_id_entry.config(state="disabled")  # Disable the entry after setting the ID

        # Close the database connection
        conn.close()

    except sqlite3.Error as e:
        # Handle any errors that occur during the database operation
        messagebox.showerror("Database Error", f"Error occurred: {e}")

# Call the generate_employee_id function when the window is initialized
generate_employee_id()


root.mainloop()
