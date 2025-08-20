from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry  # Import DateEntry for date picker
import sqlite3
import os  # To navigate between scripts

# Create the main application window
root = tk.Tk()
root.title("Edit Employee")
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
    text="Edit Employee",
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

# Row 1
is_active_label = tk.Label(signup_frame, text="Is Active:", **label_style)
is_active_label.grid(row=0, column=0, padx=10, pady=15, sticky="e")

# Create a variable to store the state of the checkbox (True or False)
is_active_var = tk.BooleanVar()

# Create the Checkbutton for isActive (True for active, False for inactive)
is_active_checkbox = tk.Checkbutton(signup_frame, variable=is_active_var, onvalue=True, offvalue=False, font=("Helvetica", 12), highlightthickness=0)
is_active_checkbox.grid(row=0, column=1, padx=10, pady=15)

# Other fields
fields = {
    "Email": {"row": 0, "column": 2},
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
    entries["Is Active"] = is_active_var
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

    first_name = entries["First Name"].get()
    last_name = entries["Last Name"].get()
    email = entries["Email"].get()
    password = entries["Password"].get()
    phone = entries["Phone"].get()
    department = entries["Department"].get()
    role_id = entries["Role ID"].get()
    manager_id = entries["Manager ID"].get()
    is_active = int(is_active_var.get())
    
    if not email or not password or not phone or not department or not first_name or not last_name or not role_id:
        messagebox.showwarning("Validation Error", "All fields are required.")
        return
    
    try:
        conn = sqlite3.connect("rbac_group6.db") 
        cursor = conn.cursor()
        
        employee_id = search_entry.get()
        
        # Check for duplicate email
        cursor.execute("""
            SELECT COUNT(*) 
            FROM Employee 
            WHERE Email = ? AND EmployeeID != ?
            """, (email, employee_id))

        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Duplicate Data", "Duplicate data - Email ID is already present.")
            return
        
        cursor.execute("SELECT COUNT(*) FROM Employee WHERE EmployeeID = ? AND RoleID <= 2", (manager_id,))
        if cursor.fetchone()[0] == 0:
            messagebox.showerror("Invalid Manager", "The entered Manager ID is invalid or does not have the Manager role.")
            return
        
        # Update data into the database
        cursor.execute("""
            UPDATE Employee
            SET 
                FirstName = ?, 
                LastName = ?, 
                Email = ?, 
                Password = ?, 
                Phone = ?, 
                Department = ?, 
                RoleID = ?, 
                ManagerID = ?, 
                IsActive = ?, 
                UpdatedOn = ?, 
                UpdatedBy = ?
            WHERE EmployeeID = ?
            """, (first_name, last_name, email, password, phone, department, role_id, manager_id, is_active, sqlite3.datetime.datetime.now(), 1, employee_id))

        conn.commit()
        messagebox.showinfo("Success", "Employee edited successfully.")
        
        # Get the most recent EmployeeID from the Log table
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
        log_message = f"Edited Employee - {first_name} {last_name}"

        # Insert the log entry into the Log table
        cursor.execute("""
            INSERT INTO Log (EmployeeID, Action, Timestamp)
            VALUES (?, ?, ?)
            """, (employee_id, log_message, sqlite3.datetime.datetime.now()))

        # Commit the changes to the database
        conn.commit()
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

# Create a new frame at the bottom for search functionality
search_frame = tk.Frame(root, bg="#1E2A47", padx=20, pady=20)
search_frame.pack(side="bottom", fill="x", pady=20)  # Position it at the bottom of the window

# Label and Entry for Employee ID Search
search_label = tk.Label(search_frame, text="Search by Employee ID:", **label_style)
search_label.grid(row=0, column=0, padx=10, pady=15, sticky="e")

search_entry = tk.Entry(search_frame, font=("Helvetica", 12), width=25, highlightthickness=0)
search_entry.grid(row=0, column=1, padx=10, pady=15)

# Function to load employee data based on EmployeeID
def load_employee_data(employee_id):
    # Database connection (adjust with your actual database)
    conn = sqlite3.connect('rbac_group6.db')  # Replace with your database path
    cursor = conn.cursor()
    
    try:
        # Query the employee data by EmployeeID
        cursor.execute("SELECT * FROM Employee WHERE EmployeeID=?", (employee_id,))
        employee_data = cursor.fetchone()

        if employee_data:
            # Populate the fields with the data from the database based on updated indices
            is_active_var.set(employee_data[10])
            
            entries["First Name"].delete(0, tk.END)
            entries["First Name"].insert(0, employee_data[1])  # index 1 is First Name
            
            entries["Last Name"].delete(0, tk.END)
            entries["Last Name"].insert(0, employee_data[2])  # index 2 is Last Name
            
            entries["Password"].delete(0, tk.END)
            entries["Password"].insert(0, employee_data[4])  # index 4 is Password
            
            entries["Phone"].delete(0, tk.END)
            entries["Phone"].insert(0, employee_data[5])  # index 5 is Phone
            
            entries["Department"].delete(0, tk.END)
            entries["Department"].insert(0, employee_data[6])  # index 6 is Department
            
            entries["Role ID"].delete(0, tk.END)
            entries["Role ID"].insert(0, employee_data[7])  # index 7 is RoleID
            
            entries["Manager ID"].delete(0, tk.END)
            entries["Manager ID"].insert(0, employee_data[9])  # index 9 is ManagerID
            
            hire_date_str = employee_data[8]
            try:
                # Convert string to datetime.date object
                hire_date = datetime.strptime(hire_date_str, "%Y-%m-%d").date()
                entries["Hire Date"].set_date(hire_date)  # Set the date in the DateEntry widget
            except ValueError:
                # Handle invalid date format (if necessary)
                print(f"Invalid date format: {hire_date_str}")
            
            # Set email as well
            entries["Email"].delete(0, tk.END)
            entries["Email"].insert(0, employee_data[3])  # index 3 is Email

        else:
            messagebox.showinfo("Error", f"No employee found with Employee ID: {employee_id}")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while fetching data: {e}")
    finally:
        conn.close()

# Search Button to trigger loading employee data
def search_employee():
    employee_id = search_entry.get()
    
    # Validate Employee ID input
    if not employee_id.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid numeric Employee ID.")
        return
    
    # Call the load_employee_data function with the entered Employee ID
    load_employee_data(employee_id)

search_button = tk.Button(search_frame, text="Search", font=("Helvetica", 12), bg="#4CAF50", fg="white", command=search_employee)
search_button.grid(row=0, column=2, padx=10, pady=15)



root.mainloop()
