import tkinter as tk
from tkinter import ttk
import sqlite3  # Use sqlite3 for SQLite database connection

# Connect to the SQLite database
conn = sqlite3.connect("rbac_group6.db")
cursor = conn.cursor()

# Create the main application window
root = tk.Tk()
root.title("Employee Log Data")
root.geometry("800x600")

# Center the window on the screen
root.eval('tk::PlaceWindow . center')

# Create the Treeview widget to display the logs (this is created once)
log_tree = ttk.Treeview(root, columns=("LogID", "EmployeeID", "Action", "Timestamp"), show="headings")
log_tree.heading("LogID", text="Log ID")
log_tree.heading("EmployeeID", text="Employee ID")
log_tree.heading("Action", text="Action")
log_tree.heading("Timestamp", text="Timestamp")
log_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Function to fetch log data from the database
def fetch_logs():
    cursor.execute("SELECT LogID, EmployeeID, Action, Timestamp FROM Log")
    logs = cursor.fetchall()
    return logs

# Function to update the log data in the Treeview
def display_logs():
    logs = fetch_logs()

    # Clear any existing logs in the Treeview
    for item in log_tree.get_children():
        log_tree.delete(item)

    # Populate the Treeview with the new log data
    for log in logs:
        log_tree.insert("", tk.END, values=log)

# Call the function to display the logs when the application starts
display_logs()

# Run the Tkinter main loop
root.mainloop()

# Close the database connection
conn.close()
