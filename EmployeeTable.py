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
# Get the latest EmployeeID from the Log table
latest_employee_id = get_latest_employee_id()

# Check permissions for the Employee table with RoleID = latest_employee_role_id
def get_employee_permissions():
    # Assuming you have a function to get the latest logged-in employee's ID
    latest_employee_id = get_latest_employee_id()  
    latest_employee_role_id = get_employee_role_id(latest_employee_id)  # Fetch the role ID for the employee
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ReadPermission, WritePermission, UpdatePermission, DeletePermission
        FROM Permission
        WHERE RoleID = ? AND TableName = 'Employee'
    """, (latest_employee_role_id,)) 
    permissions = cursor.fetchone()
    conn.close()

    # Return default permissions if none are found in the database
    if permissions is None:
        return (0, 0, 0, 0)  # No permissions by default
    return permissions

# Fetch Employee table data
def fetch_employee_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT EmployeeID, FirstName, LastName, Email, Password, Department, RoleID, IsActive FROM Employee")
    employees = cursor.fetchall()
    conn.close()
    return employees

# Insert a new employee
def add_employee(first_name, last_name, email, password, department, role_id, is_active):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Employee (FirstName, LastName, Email, Password, Department, RoleID, HireDate, ManagerID, IsActive, CreatedOn)
        VALUES (?, ?, ?, ?, ?, ?, date('now'), 1, ?, datetime('now'))
    """, (first_name, last_name, email, password, department, role_id, is_active))
    conn.commit()
    conn.close()


# Update an employee
def update_employee(emp_id, first_name, last_name, email, password, department, role_id, is_active):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Employee
        SET FirstName = ?, LastName = ?, Email = ?, Password = ?, Department = ?, RoleID = ?, IsActive = ?, UpdatedOn = datetime('now')
        WHERE EmployeeID = ?
    """, (first_name, last_name, email, password, department, role_id, is_active, emp_id))
    conn.commit()
    conn.close()


# Delete an employee
def delete_employee(emp_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Employee WHERE EmployeeID = ?", (emp_id,))
    conn.commit()
    conn.close()


# GUI to display and manage the Employee table
def employee_table_gui():
    def refresh_table():
        """Refresh the data in the Treeview."""
        for row in tree.get_children():
            tree.delete(row)
        employees = fetch_employee_data()
        for emp in employees:
            tree.insert("", "end", values=emp)

    def add_entry():
        """Add a new employee to the database."""
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        department = department_entry.get()
        role_id = role_id_entry.get()
        is_active = is_active_var.get()

        if first_name and last_name and email and password and department and role_id.isdigit():
            add_employee(first_name, last_name, email, password, department, int(role_id), is_active)
            refresh_table()
            clear_fields()
        else:
            messagebox.showerror("Error", "Please fill in all fields and ensure Role ID is an integer.")

    def update_entry():
        """Update an employee's details."""
        selected_item = tree.selection()
        if selected_item:
            emp_id = tree.item(selected_item[0], "values")[0]
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            department = department_entry.get()
            role_id = role_id_entry.get()
            is_active = is_active_var.get()

            if first_name and last_name and email and password and department and role_id.isdigit():
                update_employee(emp_id, first_name, last_name, email, password, department, int(role_id), is_active)
                refresh_table()
                clear_fields()
            else:
                messagebox.showerror("Error", "Please fill in all fields and ensure Role ID is an integer.")
        else:
            messagebox.showerror("Error", "Please select an employee to update.")

    def delete_entry():
        """Delete an employee from the database."""
        selected_item = tree.selection()
        if selected_item:
            emp_id = tree.item(selected_item[0], "values")[0]
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this employee?"):
                delete_employee(emp_id)
                refresh_table()
                clear_fields()
        else:
            messagebox.showerror("Error", "Please select an employee to delete.")

    def clear_fields():
        """Clear all input fields."""
        first_name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        department_entry.delete(0, tk.END)
        role_id_entry.delete(0, tk.END)
        is_active_var.set(1)

    def populate_fields(event):
        """Populate the fields with the selected employee's data."""
        selected_item = tree.selection()
        if selected_item:
            emp_id, first_name, last_name, email, password, department, role_id, is_active = tree.item(selected_item[0], "values")
            first_name_entry.delete(0, tk.END)
            first_name_entry.insert(0, first_name)

            last_name_entry.delete(0, tk.END)
            last_name_entry.insert(0, last_name)

            email_entry.delete(0, tk.END)
            email_entry.insert(0, email)

            password_entry.delete(0, tk.END)
            password_entry.insert(0, password)

            department_entry.delete(0, tk.END)
            department_entry.insert(0, department)

            role_id_entry.delete(0, tk.END)
            role_id_entry.insert(0, role_id)

            is_active_var.set(is_active)

    # Main Window
    root = tk.Tk()
    root.title("Employee Management")
    root.geometry("900x600")

    # Treeview for Employee Table
    columns = ("EmployeeID", "FirstName", "LastName", "Email", "Password", "Department", "RoleID", "IsActive")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill="both", expand=True, pady=10)
    tree.bind("<<TreeviewSelect>>", populate_fields)

    # Input Fields
    form_frame = tk.Frame(root)
    form_frame.pack(fill="x", pady=10)

    tk.Label(form_frame, text="First Name:").grid(row=0, column=0, padx=5, pady=5)
    first_name_entry = tk.Entry(form_frame)
    first_name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Last Name:").grid(row=1, column=0, padx=5, pady=5)
    last_name_entry = tk.Entry(form_frame)
    last_name_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
    email_entry = tk.Entry(form_frame)
    email_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Password:").grid(row=3, column=0, padx=5, pady=5)
    password_entry = tk.Entry(form_frame, show="*")
    password_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Department:").grid(row=4, column=0, padx=5, pady=5)
    department_entry = tk.Entry(form_frame)
    department_entry.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Role ID:").grid(row=5, column=0, padx=5, pady=5)
    role_id_entry = tk.Entry(form_frame)
    role_id_entry.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Is Active:").grid(row=6, column=0, padx=5, pady=5)
    is_active_var = tk.IntVar(value=1)
    is_active_checkbox = tk.Checkbutton(form_frame, variable=is_active_var)
    is_active_checkbox.grid(row=6, column=1, padx=5, pady=5)

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(fill="x", pady=10)

    tk.Button(button_frame, text="Add", command=add_entry).grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Update", command=update_entry).grid(row=0, column=1, padx=10)
    # tk.Button(button_frame, text="Delete", command=delete_entry).grid(row=0, column=2, padx=10)
    tk.Button(button_frame, text="Refresh", command=refresh_table).grid(row=0, column=3, padx=10)

    refresh_table()
    root.mainloop()


# Run the GUI
employee_table_gui()