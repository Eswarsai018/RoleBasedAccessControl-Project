import tkinter as tk
from tkinter import ttk
import sqlite3  # Use sqlite3 for SQLite database connection

# Connect to the SQLite database
conn = sqlite3.connect("rbac_group6.db")
cursor = conn.cursor()

# Create the main application window
root = tk.Tk()
root.title("Special Access Data")
root.geometry("1000x600")  # Adjust the window size to fit more data

# Center the window on the screen
root.eval('tk::PlaceWindow . center')

# Create the Treeview widget to display the special access data with new columns
special_access_tree = ttk.Treeview(
    root,
    columns=("SpecialAccessID", "EmployeeID", "EmployeeName", "SpecialAccessApplication", 
             "Approval", "IsActive", "CreatedOn", "CreatedBy", "UpdatedOn", "UpdatedBy"),
    show="headings"
)

# Define the column headings
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

# Adjust column widths to fit the content
special_access_tree.column("SpecialAccessID", width=100)
special_access_tree.column("EmployeeID", width=100)
special_access_tree.column("EmployeeName", width=200)
special_access_tree.column("SpecialAccessApplication", width=200)
special_access_tree.column("Approval", width=80)
special_access_tree.column("IsActive", width=80)
special_access_tree.column("CreatedOn", width=150)
special_access_tree.column("CreatedBy", width=150)
special_access_tree.column("UpdatedOn", width=150)
special_access_tree.column("UpdatedBy", width=150)

special_access_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Function to fetch special access data from the database
def fetch_special_access_data():
    cursor.execute("""
        SELECT sa.SpecialAccessID, e.EmployeeID, e.FirstName || ' ' || e.LastName AS EmployeeName,
               sa.SpecialAccessApplication, sa.Approval, sa.IsActive, sa.CreatedOn, sa.CreatedBy, 
               sa.UpdatedOn, sa.UpdatedBy
        FROM SpecialAccess sa
        JOIN Employee e ON sa.EmployeeID = e.EmployeeID
        ORDER BY sa.CreatedOn DESC;
    """)
    special_access_data = cursor.fetchall()
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

# Call the function to display the special access data when the application starts
display_special_access_data()

# Run the Tkinter main loop
root.mainloop()

# Close the database connection
conn.close()
