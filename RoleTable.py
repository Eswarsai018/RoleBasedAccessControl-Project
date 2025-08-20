import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Connect to the SQLite database
def connect_db():
    return sqlite3.connect("rbac_group6.db")

def get_latest_employee_id():
    # Connect to the SQLite database
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

# Check permissions for the Role table with RoleID = latest_employee_role_id
def get_role_permissions():
    latest_employee_id = get_latest_employee_id()
    latest_employee_role_id = get_employee_role_id(latest_employee_id)  # Fetch the role ID for the employee
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ReadPermission, WritePermission, UpdatePermission, DeletePermission
        FROM Permission
        WHERE RoleID = ? AND TableName = 'Role'
    """, (latest_employee_role_id,))
    permissions = cursor.fetchone()
    conn.close()

    # Return default permissions if none are found in the database
    if permissions is None:
        return (0, 0, 0, 0)  # No permissions by default
    return permissions

# Fetch Role table data
def fetch_role_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT RoleID, RoleName, Description, CreatedOn, UpdatedOn FROM Role")
    roles = cursor.fetchall()
    conn.close()
    return roles

# Insert a new role
def add_role(role_name, description):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Role (RoleName, Description, CreatedOn, UpdatedOn)
        VALUES (?, ?, datetime('now'), datetime('now'))
    """, (role_name, description))
    conn.commit()
    conn.close()

# Update a role
def update_role(role_id, role_name, description):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Role
        SET RoleName = ?, Description = ?, UpdatedOn = datetime('now')
        WHERE RoleID = ?
    """, (role_name, description, role_id))
    conn.commit()
    conn.close()

# Delete a role
def delete_role(role_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Role WHERE RoleID = ?", (role_id,))
    conn.commit()
    conn.close()

# GUI for Role Table
def role_table_gui():
    permissions = get_role_permissions()
    read, write, update, delete = permissions

    def refresh_table():
        if read:
            for row in tree.get_children():
                tree.delete(row)
            roles = fetch_role_data()
            for role in roles:
                tree.insert("", "end", values=role)
        else:
            messagebox.showerror("Error", "You do not have permission to read the Role table.")
            root.destroy()

    def add_entry():
        if write:
            role_name = role_name_entry.get()
            description = description_entry.get()

            if role_name:
                add_role(role_name, description)
                refresh_table()
                clear_fields()
            else:
                messagebox.showerror("Error", "Role Name is required.")
        else:
            messagebox.showerror("Error", "You do not have permission to add roles.")

    def update_entry():
        if update:
            selected_item = tree.selection()
            if selected_item:
                role_id = tree.item(selected_item[0], "values")[0]
                role_name = role_name_entry.get()
                description = description_entry.get()

                if role_name:
                    update_role(role_id, role_name, description)
                    refresh_table()
                    clear_fields()
                else:
                    messagebox.showerror("Error", "Role Name is required.")
            else:
                messagebox.showerror("Error", "Please select a role to update.")
        else:
            messagebox.showerror("Error", "You do not have permission to update roles.")

    def delete_entry():
        if delete:
            selected_item = tree.selection()
            if selected_item:
                role_id = tree.item(selected_item[0], "values")[0]
                if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this role?"):
                    delete_role(role_id)
                    refresh_table()
                    clear_fields()
            else:
                messagebox.showerror("Error", "Please select a role to delete.")
        else:
            messagebox.showerror("Error", "You do not have permission to delete roles.")

    def clear_fields():
        role_name_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)

    def populate_fields(event):
        selected_item = tree.selection()
        if selected_item:
            role_id, role_name, description, created_on, updated_on = tree.item(selected_item[0], "values")
            role_name_entry.delete(0, tk.END)
            role_name_entry.insert(0, role_name)

            description_entry.delete(0, tk.END)
            description_entry.insert(0, description)

    root = tk.Tk()
    root.title("Role Management")
    root.geometry("800x600")

    # Treeview for Role Table
    columns = ("RoleID", "RoleName", "Description", "CreatedOn", "UpdatedOn")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill="both", expand=True, pady=10)
    tree.bind("<<TreeviewSelect>>", populate_fields)

    # Input Fields
    form_frame = tk.Frame(root)
    form_frame.pack(fill="x", pady=10)

    tk.Label(form_frame, text="Role Name:").grid(row=0, column=0, padx=5, pady=5)
    role_name_entry = tk.Entry(form_frame)
    role_name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5)
    description_entry = tk.Entry(form_frame)
    description_entry.grid(row=1, column=1, padx=5, pady=5)

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(fill="x", pady=10)

    tk.Button(button_frame, text="Add", command=add_entry).grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Update", command=update_entry).grid(row=0, column=1, padx=10)
    tk.Button(button_frame, text="Delete", command=delete_entry).grid(row=0, column=2, padx=10)
    tk.Button(button_frame, text="Refresh", command=refresh_table).grid(row=0, column=3, padx=10)

    refresh_table()
    root.mainloop()

# Run the GUI
role_table_gui()
