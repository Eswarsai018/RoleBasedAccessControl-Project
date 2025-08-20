import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os  # To open external scripts
import sys
import sqlite3  # Add SQLite connection to interact with the database

# RoleID will be passed as an argument when calling mainpage.py (e.g., os.system("python mainpage.py 3"))
role_id = sys.argv[1] if len(sys.argv) > 1 else "0"  # Default to "0" if not provided

# Function to check Special Access from the database
def check_special_access(employee_id, special_access_application):
    # Connect to the SQLite database (adjust the path if necessary)
    conn = sqlite3.connect('rbac_group6.db')
    cursor = conn.cursor()

    try:
        # Query the SpecialAccess table for the relevant EmployeeID and check the conditions
        cursor.execute("""
            SELECT SpecialAccessApplication, Approval, IsActive
            FROM SpecialAccess
            WHERE EmployeeID = ? 
            AND SpecialAccessApplication = ?
        """, (employee_id, special_access_application))
        result = cursor.fetchone()

        # If the result exists and meets the conditions (Approval = True and IsActive = True)
        if result and result[1] == 1 and result[2] == 1:  # Approval and IsActive are True
            return True
        return False

    finally:
        conn.close()
        
# Function to get the latest employee ID from the Log table
def get_latest_employee_id():
    # Connect to the SQLite database (adjust the path if necessary)
    conn = sqlite3.connect('rbac_group6.db')
    cursor = conn.cursor()

    # Query to get the latest employee ID from the Log table
    cursor.execute("""
        SELECT EmployeeID
        FROM Log
        ORDER BY LogID DESC
        LIMIT 1
        """)
    result = cursor.fetchone()
    
    if result:
        conn.close()
        return result[0]  # Return EmployeeID of the latest entry
    conn.close()
    return None

# Function to get the RoleID of an employee from the Employee table
def get_employee_role_id(employee_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('rbac_group6.db')
    cursor = conn.cursor()

    # Query to get the RoleID from the Employee table based on EmployeeID
    cursor.execute("""
        SELECT RoleID
        FROM Employee
        WHERE EmployeeID = ?
        """, (employee_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]  # Return the RoleID
    return None
# Get the latest EmployeeID from the Log table
latest_employee_id = get_latest_employee_id()

# Get the RoleID of the latest employee
latest_employee_role_id = get_employee_role_id(latest_employee_id)

# Create the main application window
root = tk.Tk()
root.title("Dashboard")
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

# Title label style with custom colors (professional)
title_label = tk.Label(
    root,
    text="Dashboard",
    font=("Helvetica", 24, "bold", "underline"),
    fg="#A7A9B7",  # Light gray color for text (professional)
    bg="#1E2A47",  # Dark blue background (professional)
    padx=20,
    pady=10
)
title_label.pack(fill="x", pady=20)

# Function for logout
def logout():
    if messagebox.askyesno("Logout Confirmation", "Are you sure you want to log out?"):
        root.destroy()  # Close the current window
        os.system("python LogInPage.py")  # Open the login page

# Add the Logout button
logout_button = tk.Button(
    root,
    text="Logout",
    font=("Helvetica", 10, "bold"),
    bg="#FF4D4D",  # Red background for the logout button
    fg="white",
    command=logout
)
logout_button.place(relx=0.95, rely=0.05, anchor="ne")  # Top-right corner of the screen

# Create a frame for the database buttons
db_group_frame = tk.Frame(root, bg="#1E2A47", padx=20, pady=20)
db_group_frame.pack(fill="both", expand=True)

# Database group section
db_group_label = tk.Label(db_group_frame, text="Database", font=("Helvetica", 16, "bold"), fg="#A7A9B7", bg="#1E2A47")
db_group_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

# Database table buttons
def open_employee_table():
    os.system("python EmployeeTable.py")
def open_role_table():
    os.system("python RoleTable.py")
def open_permission_table():
    os.system("python PermissionTable.py")
def open_access_table():
    os.system("python AccessTable.py")
    
employee_table_button = tk.Button(db_group_frame, text="Employee Table", font=("Helvetica", 12), width=20, command=open_employee_table)
employee_table_button.grid(row=1, column=0, padx=10, pady=10)

role_table_button = tk.Button(db_group_frame, text="Role Table", font=("Helvetica", 12), width=20, command=open_role_table)
role_table_button.grid(row=1, column=1, padx=10, pady=10)

permission_table_button = tk.Button(db_group_frame, text="Permission Table", font=("Helvetica", 12), width=20, command=open_permission_table)
permission_table_button.grid(row=2, column=0, padx=10, pady=10)

access_table_button = tk.Button(db_group_frame, text="Access Table", font=("Helvetica", 12), width=20, command=open_access_table)
access_table_button.grid(row=2, column=1, padx=10, pady=10)

# Create a frame for the rest of the buttons (outside of the database group)
other_buttons_frame = tk.Frame(root, bg="#1E2A47", padx=20, pady=20)
other_buttons_frame.pack(fill="both", expand=True)

# Log data button
def open_log_data_application():
    os.system("python logdata.py")

log_data_button = tk.Button(other_buttons_frame, text="Log Data", font=("Helvetica", 12), width=20, command=open_log_data_application)
log_data_button.grid(row=1, column=0, padx=10, pady=10)

# Special Access data button
def open_special_access_data_application():
    os.system("python SpecialAccessData.py")
    
special_access_button = tk.Button(other_buttons_frame, text="Special Access Data", font=("Helvetica", 12), width=20, command=open_special_access_data_application)
special_access_button.grid(row=1, column=1, padx=10, pady=10)

# Data Application button
def open_date_application():
    os.system("python displaycurrentdate.py")

date_application_button = tk.Button(
    other_buttons_frame, text="Date Application", font=("Helvetica", 12), width=20, command=open_date_application
)
date_application_button.grid(row=2, column=0, padx=10, pady=10)

# Clock Application button
def open_clock_application():
    os.system("python clock.py")

clock_application_button = tk.Button(
    other_buttons_frame, text="Clock Application", font=("Helvetica", 12), width=20, command=open_clock_application
)
clock_application_button.grid(row=2, column=1, padx=10, pady=10)

def open_special_access_request_application():
    os.system("python SpecialAccessRequest.py")
    
def open_special_access_grant_application():
    os.system("python SpecialAccessGranting.py")

if latest_employee_role_id == 3:
    special_access_request_button = tk.Button(other_buttons_frame, text="Special Access Request", font=("Helvetica", 12), width=20, command=open_special_access_request_application)
    special_access_request_button.grid(row=3, column=0, padx=10, pady=10)
    
if latest_employee_role_id == 2:
    special_access_request_button = tk.Button(other_buttons_frame, text="Special Access Granting", font=("Helvetica", 12), width=20, command=open_special_access_grant_application)
    special_access_request_button.grid(row=3, column=0, padx=10, pady=10)
# Disable buttons based on Role ID and SpecialAccess
if latest_employee_role_id >= 3:
    # Check if the employee has special access for 'Date Application'
    if not check_special_access(latest_employee_id, 'Date Application'):
        date_application_button.config(state="disabled")
    
    # Check if the employee has special access for 'Clock Application'
    if not check_special_access(latest_employee_id, 'Clock Application'):
        clock_application_button.config(state="disabled")
    
    # Check if the employee has special access for 'Special Access Data'
    if not check_special_access(latest_employee_id, 'Special Access Data'):
        special_access_button.config(state="disabled")
        
    if not check_special_access(latest_employee_id, 'Log Data'):
        log_data_button.config(state="disabled")

# Add Create Employee and Edit Employee buttons only if RoleID is 1
if latest_employee_role_id == 1:
    # Create Employee Button
    create_employee_button = tk.Button(
        other_buttons_frame,
        text="Create Employee",
        font=("Helvetica", 12),
        width=20,
        command=lambda: [root.destroy(), os.system("python CreateEmployee.py")]
    )
    create_employee_button.grid(row=0, column=0, padx=10, pady=10)

    # Edit Employee Button
    edit_employee_button = tk.Button(
        other_buttons_frame,
        text="Edit Employee",
        font=("Helvetica", 12),
        width=20,
        command=lambda: [root.destroy(), os.system("python EditEmployee.py")]
    )
    edit_employee_button.grid(row=0, column=1, padx=10, pady=10)
else:
    # If the RoleID is not 1, these buttons won't appear.
    pass

# Function to handle button clicks
def on_click(button_name):
    messagebox.showinfo("Button Clicked", f"You clicked: {button_name}")

# Start the main event loop
root.mainloop()
