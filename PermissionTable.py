import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Connect to the SQLite database
def connect_db():
    return sqlite3.connect("rbac_group6.db")

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

def get_permissions_for_table(table_name):
    latest_employee_id = get_latest_employee_id()
    latest_employee_role_id = get_employee_role_id(latest_employee_id)
    
    conn = sqlite3.connect('rbac_group6.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ReadPermission, WritePermission, UpdatePermission, DeletePermission
        FROM Permission
        WHERE RoleID = ? AND TableName = ?
    """, (latest_employee_role_id, table_name))
    permissions = cursor.fetchone()
    conn.close()
    
    if permissions is None:
        return (0, 0, 0, 0)  # Default: No permissions
    return permissions

# Fetch Permission table data
def fetch_permission_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT PermissionID, RoleID, TableName, ReadPermission, WritePermission, UpdatePermission, DeletePermission, CreatedOn, UpdatedOn
        FROM Permission
    """)
    permissions = cursor.fetchall()
    conn.close()
    return permissions

# Insert a new permission
def add_permission(role_id, table_name, read_permission, write_permission, update_permission, delete_permission):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Permission (RoleID, TableName, ReadPermission, WritePermission, UpdatePermission, DeletePermission, CreatedOn, UpdatedOn)
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
    """, (role_id, table_name, read_permission, write_permission, update_permission, delete_permission))
    conn.commit()
    conn.close()

# Update a permission
def update_permission(permission_id, role_id, table_name, read_permission, write_permission, update_permission, delete_permission):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Permission
        SET RoleID = ?, TableName = ?, ReadPermission = ?, WritePermission = ?, UpdatePermission = ?, DeletePermission = ?, UpdatedOn = datetime('now')
        WHERE PermissionID = ?
    """, (role_id, table_name, read_permission, write_permission, update_permission, delete_permission, permission_id))
    conn.commit()
    conn.close()

# Delete a permission
def delete_permission(permission_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Permission WHERE PermissionID = ?", (permission_id,))
    conn.commit()
    conn.close()

# GUI for Permission Table
def permission_table_gui():
    permissions = get_permissions_for_table("Permission")
    read, write, update, delete = permissions

    def refresh_table():
        if read:
            for row in tree.get_children():
                tree.delete(row)
            permissions = fetch_permission_data()
            for perm in permissions:
                tree.insert("", "end", values=perm)
        else:
            messagebox.showerror("Error", "You do not have permission to read the Permission table.")
            root.destroy()

    def add_entry():
        if write:
            role_id = role_id_entry.get()
            table_name = table_name_entry.get()
            read_perm = read_permission_var.get()
            write_perm = write_permission_var.get()
            update_perm = update_permission_var.get()
            delete_perm = delete_permission_var.get()

            if not role_id.isdigit():
                messagebox.showerror("Error", "Role ID must be an integer.")
                return
            if not table_name.strip():
                messagebox.showerror("Error", "Table Name cannot be empty.")
                return

            add_permission(int(role_id), table_name.strip(), read_perm, write_perm, update_perm, delete_perm)
            refresh_table()
            clear_fields()
            messagebox.showinfo("Success", "Permission added successfully!")
        else:
            messagebox.showerror("Error", "You do not have permission to add permissions.")


    def update_entry():
        if update:
            selected_item = tree.selection()
            if selected_item:
                permission_id = tree.item(selected_item[0], "values")[0]
                role_id = role_id_entry.get()
                table_name = table_name_entry.get()
                read_perm = read_permission_var.get()
                write_perm = write_permission_var.get()
                update_perm = update_permission_var.get()
                delete_perm = delete_permission_var.get()

                if role_id.isdigit() and table_name:
                    update_permission(permission_id, int(role_id), table_name, read_perm, write_perm, update_perm, delete_perm)
                    refresh_table()
                    clear_fields()
                else:
                    messagebox.showerror("Error", "Please fill in all fields and ensure Role ID is an integer.")
            else:
                messagebox.showerror("Error", "Please select a permission to update.")
        else:
            messagebox.showerror("Error", "You do not have permission to update permissions.")

    def delete_entry():
        if delete:
            selected_item = tree.selection()
            if selected_item:
                permission_id = tree.item(selected_item[0], "values")[0]
                if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this permission?"):
                    delete_permission(permission_id)
                    refresh_table()
            else:
                messagebox.showerror("Error", "Please select a permission to delete.")
        else:
            messagebox.showerror("Error", "You do not have permission to delete permissions.")

    def clear_fields():
        role_id_entry.delete(0, tk.END)
        table_name_entry.delete(0, tk.END)
        read_permission_var.set(0)
        write_permission_var.set(0)
        update_permission_var.set(0)
        delete_permission_var.set(0)

    def populate_fields(event):
        selected_item = tree.selection()
        if selected_item:
            permission_id, role_id, table_name, read_permission, write_permission, update_permission, delete_permission, created_on, updated_on = tree.item(selected_item[0], "values")
            role_id_entry.delete(0, tk.END)
            role_id_entry.insert(0, role_id)

            table_name_entry.delete(0, tk.END)
            table_name_entry.insert(0, table_name)

            read_permission_var.set(read_permission)
            write_permission_var.set(write_permission)
            update_permission_var.set(update_permission)
            delete_permission_var.set(delete_permission)

    root = tk.Tk()
    root.title("Permission Management")
    root.geometry("900x600")

    # Treeview for Permission Table
    columns = ("PermissionID", "RoleID", "TableName", "ReadPermission", "WritePermission", "UpdatePermission", "DeletePermission", "CreatedOn", "UpdatedOn")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill="both", expand=True, pady=10)
    tree.bind("<<TreeviewSelect>>", populate_fields)

    # Input Fields
    form_frame = tk.Frame(root)
    form_frame.pack(fill="x", pady=10)

    tk.Label(form_frame, text="Role ID:").grid(row=0, column=0, padx=5, pady=5)
    role_id_entry = tk.Entry(form_frame)
    role_id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Table Name:").grid(row=1, column=0, padx=5, pady=5)
    table_name_entry = tk.Entry(form_frame)
    table_name_entry.grid(row=1, column=1, padx=5, pady=5)

    read_permission_var = tk.IntVar(value=0)
    write_permission_var = tk.IntVar(value=0)
    update_permission_var = tk.IntVar(value=0)
    delete_permission_var = tk.IntVar(value=0)

    tk.Checkbutton(form_frame, text="Read", variable=read_permission_var).grid(row=2, column=0, padx=5, pady=5)
    tk.Checkbutton(form_frame, text="Write", variable=write_permission_var).grid(row=2, column=1, padx=5, pady=5)
    tk.Checkbutton(form_frame, text="Update", variable=update_permission_var).grid(row=2, column=2, padx=5, pady=5)
    tk.Checkbutton(form_frame, text="Delete", variable=delete_permission_var).grid(row=2, column=3, padx=5, pady=5)

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
permission_table_gui()
