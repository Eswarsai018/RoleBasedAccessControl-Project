import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime  # Import datetime module for the current timestamp

# Create the main application window for Special Access Granting page
granting_root = tk.Tk()
granting_root.title("Special Access Granting")

# Set the window size to be large enough to display the data clearly
granting_root.geometry("1000x600")  # Width x Height (Adjust as needed)

# Center the window on the screen
granting_root.eval('tk::PlaceWindow . center')

def fetch_log_employee_id():
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
            
    return employee_id_log
    
# Function to fetch special access data from the database
def fetch_special_access_data():
    conn = sqlite3.connect("rbac_group6.db")
    cursor = conn.cursor()
    employee_id_log = fetch_log_employee_id()  # Get the employee ID from the log table

    cursor.execute("""
        SELECT sa.SpecialAccessID, e.EmployeeID, e.FirstName || ' ' || e.LastName AS EmployeeName, 
               sa.SpecialAccessApplication, sa.Approval, sa.IsActive, sa.CreatedOn, sa.CreatedBy, sa.UpdatedOn, sa.UpdatedBy
        FROM SpecialAccess sa
        JOIN Employee e ON sa.EmployeeID = e.EmployeeID
        WHERE e.ManagerID = ?  -- Only show records where ManagerID matches employee_id_log
        ORDER BY sa.CreatedOn DESC;
    """, (employee_id_log,))  # Pass the employee_id_log as a parameter to the query

    special_access_data = cursor.fetchall()
    conn.close()
    return special_access_data


# Function to update the special access data in the Treeview
def display_special_access_data():
    special_access_data = fetch_special_access_data()

    # Clear any existing data in the Treeview
    for item in special_access_tree.get_children():
        special_access_tree.delete(item)

    # Populate the Treeview with the new data
    for record in special_access_data:
        special_access_tree.insert("", tk.END, values=record)

# Function to update approval and active status in the database
def update_special_access():
    selected_item = special_access_tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a special access request to update.")
        return

    special_access_id = special_access_tree.item(selected_item, "values")[0]
    approval = 1 if approval_var.get() else 0  # Convert boolean to 1 or 0
    is_active = 1 if is_active_var.get() else 0  # Convert boolean to 1 or 0

    conn = sqlite3.connect("rbac_group6.db")
    cursor = conn.cursor()
    
    try:
        employee_id_log = fetch_log_employee_id()
        
        # Update SpecialAccess with approval status, active status, and audit info
        cursor.execute("""
            UPDATE SpecialAccess
            SET Approval = ?, IsActive = ?, UpdatedOn = ?, UpdatedBy = ?
            WHERE SpecialAccessID = ?;
            """, (approval, is_active, datetime.now(), employee_id_log, special_access_id))
        conn.commit()
        
        employee_id_log = fetch_log_employee_id()
        
        log_message = f"Granted Special Access"
        cursor.execute("""
            INSERT INTO Log (EmployeeID, Action, Timestamp)
            VALUES (?, ?, ?)
            """, (employee_id_log, log_message, sqlite3.datetime.datetime.now()))
        conn.commit()
        
        messagebox.showinfo("Success", "Special Access updated successfully!")
        display_special_access_data()  # Refresh the Treeview with updated data
        
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Database error: {e}")
    finally:
        conn.close()

# Create the Treeview widget to display the special access data
special_access_tree = ttk.Treeview(granting_root, columns=("SpecialAccessID", "EmployeeID", "EmployeeName", "SpecialAccessApplication", "Approval", "IsActive", "CreatedOn", "CreatedBy", "UpdatedOn", "UpdatedBy"), show="headings")
special_access_tree.heading("SpecialAccessID", text="Special Access ID")
special_access_tree.heading("EmployeeID", text="Employee ID")
special_access_tree.heading("EmployeeName", text="Employee Name")
special_access_tree.heading("SpecialAccessApplication", text="Application")
special_access_tree.heading("Approval", text="Approval")
special_access_tree.heading("IsActive", text="Is Active")
special_access_tree.heading("CreatedOn", text="Created On")
special_access_tree.heading("CreatedBy", text="Created By")
special_access_tree.heading("UpdatedOn", text="Updated On")
special_access_tree.heading("UpdatedBy", text="Updated By")

# Adjust column widths to make sure all data is visible
special_access_tree.column("SpecialAccessID", width=100)
special_access_tree.column("EmployeeID", width=100)
special_access_tree.column("EmployeeName", width=200)
special_access_tree.column("SpecialAccessApplication", width=200)
special_access_tree.column("Approval", width=100)
special_access_tree.column("IsActive", width=100)
special_access_tree.column("CreatedOn", width=150)
special_access_tree.column("CreatedBy", width=100)
special_access_tree.column("UpdatedOn", width=150)
special_access_tree.column("UpdatedBy", width=100)

special_access_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Add Approval and IsActive columns as checkboxes
approval_var = tk.BooleanVar()
is_active_var = tk.BooleanVar()

approval_check_button = tk.Checkbutton(granting_root, text="Approve", variable=approval_var)
approval_check_button.pack(side=tk.LEFT, padx=10)

is_active_check_button = tk.Checkbutton(granting_root, text="Activate", variable=is_active_var)
is_active_check_button.pack(side=tk.LEFT, padx=10)

# Submit button to update the special access data
submit_button = tk.Button(granting_root, text="Submit Changes", font=("Helvetica", 12), command=update_special_access)
submit_button.pack(side=tk.LEFT, padx=10, pady=20)

# Call the function to display the special access data when the application starts
display_special_access_data()

# Start the main event loop
granting_root.mainloop()
