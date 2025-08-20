import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Connect to the SQLite database
def connect_db():
    return sqlite3.connect("rbac_group6.db")

def get_latest_employee_id():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT EmployeeID
        FROM Log
        ORDER BY LogID DESC
        LIMIT 1
    """)
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_employee_role_id(employee_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT RoleID
        FROM Employee
        WHERE EmployeeID = ?
    """, (employee_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_permissions_for_table(table_name):
    latest_employee_id = get_latest_employee_id()
    latest_employee_role_id = get_employee_role_id(latest_employee_id)
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ReadPermission, WritePermission, UpdatePermission, DeletePermission
        FROM Permission
        WHERE RoleID = ? AND TableName = ?
    """, (latest_employee_role_id, table_name))
    permissions = cursor.fetchone()
    conn.close()
    return permissions if permissions else (0, 0, 0, 0)

# Fetch Access table data
def fetch_access_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT AccessID, RoleID, Application, CreatedOn, UpdatedOn
        FROM Access
    """)
    access_entries = cursor.fetchall()
    conn.close()
    return access_entries

# Insert a new access entry
def add_access(role_id, application):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Access (RoleID, Application, CreatedOn, UpdatedOn)
        VALUES (?, ?, datetime('now'), datetime('now'))
    """, (role_id, application))
    conn.commit()
    conn.close()

# Update an access entry
def update_access(access_id, role_id, application):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Access
        SET RoleID = ?, Application = ?, UpdatedOn = datetime('now')
        WHERE AccessID = ?
    """, (role_id, application, access_id))
    conn.commit()
    conn.close()

# Delete an access entry
def delete_access(access_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Access WHERE AccessID = ?", (access_id,))
    conn.commit()
    conn.close()

# GUI for Access Table
def access_table_gui():
    permissions = get_permissions_for_table("Access")
    read, write, update, delete = permissions

    def refresh_table():
        if read:
            for row in tree.get_children():
                tree.delete(row)
            access_entries = fetch_access_data()
            for entry in access_entries:
                tree.insert("", "end", values=entry)
        else:
            messagebox.showerror("Error", "You do not have permission to read the Access table.")
            root.destroy()

    def add_entry():
        if write:
            role_id = role_id_entry.get()
            application = application_entry.get()

            if role_id.isdigit() and application.strip():
                add_access(int(role_id), application.strip())
                refresh_table()
                clear_fields()
                messagebox.showinfo("Success", "Access entry added successfully!")
            else:
                messagebox.showerror("Error", "Please fill in all fields and ensure Role ID is an integer.")
        else:
            messagebox.showerror("Error", "You do not have permission to add access entries.")

    def update_entry():
        if update:
            selected_item = tree.selection()
            if selected_item:
                access_id = tree.item(selected_item[0], "values")[0]
                role_id = role_id_entry.get()
                application = application_entry.get()

                if role_id.isdigit() and application.strip():
                    update_access(access_id, int(role_id), application.strip())
                    refresh_table()
                    clear_fields()
                    messagebox.showinfo("Success", "Access entry updated successfully!")
                else:
                    messagebox.showerror("Error", "Please fill in all fields and ensure Role ID is an integer.")
            else:
                messagebox.showerror("Error", "Please select an access entry to update.")
        else:
            messagebox.showerror("Error", "You do not have permission to update access entries.")

    def delete_entry():
        if delete:
            selected_item = tree.selection()
            if selected_item:
                access_id = tree.item(selected_item[0], "values")[0]
                if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this access entry?"):
                    delete_access(access_id)
                    refresh_table()
            else:
                messagebox.showerror("Error", "Please select an access entry to delete.")
        else:
            messagebox.showerror("Error", "You do not have permission to delete access entries.")

    def clear_fields():
        role_id_entry.delete(0, tk.END)
        application_entry.delete(0, tk.END)

    def populate_fields(event):
        selected_item = tree.selection()
        if selected_item:
            access_id, role_id, application, created_on, updated_on = tree.item(selected_item[0], "values")
            role_id_entry.delete(0, tk.END)
            role_id_entry.insert(0, role_id)

            application_entry.delete(0, tk.END)
            application_entry.insert(0, application)

    root = tk.Tk()
    root.title("Access Management")
    root.geometry("900x600")

    # Treeview for Access Table
    columns = ("AccessID", "RoleID", "Application", "CreatedOn", "UpdatedOn")
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

    tk.Label(form_frame, text="Application:").grid(row=1, column=0, padx=5, pady=5)
    application_entry = tk.Entry(form_frame)
    application_entry.grid(row=1, column=1, padx=5, pady=5)

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(fill="x", pady=10)

    # tk.Button(button_frame, text="Add", command=add_entry).grid(row=0, column=0, padx=10)
    # tk.Button(button_frame, text="Update", command=update_entry).grid(row=0, column=1, padx=10)
    # tk.Button(button_frame, text="Delete", command=delete_entry).grid(row=0, column=2, padx=10)
    tk.Button(button_frame, text="Refresh", command=refresh_table).grid(row=0, column=3, padx=10)

    refresh_table()
    root.mainloop()

# Run the GUI
access_table_gui()
