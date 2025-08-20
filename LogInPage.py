import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3  # Import the SQLite library
import os

# Create the main application window
root = tk.Tk()
root.title("Login Window")
root.geometry("700x400")  # Set the initial size of the window

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

# Title label style with custom colors
title_label = tk.Label(
    root,
    text="Hedge Fund Company",
    font=("Helvetica", 24, "bold", "underline"),
    fg="#FFFFFF",  # White text
    bg="#002B5C",  # Navy blue background
    padx=20,
    pady=10
)
title_label.pack(fill="x", pady=10)  # Expand horizontally to fill the top of the window

# Create a frame for the login fields to center them
login_frame = tk.Frame(root, bg="#007F5F", padx=10, pady=10)  # Dark green background
login_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

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

# Variables to track the email and password fields
email_var = tk.StringVar()
password_var = tk.StringVar()

# Function to enable/disable the submit button
def toggle_submit_button(*args):
    email = email_var.get().strip()
    password = password_var.get().strip()
    if email and password and email != "Enter your email" and password != "Enter Password":  # Both fields are filled
        submit_button.config(state="normal")  # Enable the button
    else:
        submit_button.config(state="disabled")  # Disable the button

# Attach the function to changes in the email and password variables
email_var.trace_add("write", toggle_submit_button)
password_var.trace_add("write", toggle_submit_button)

# Label and Entry for Email
mail_label = tk.Label(login_frame, text="Mail:", font=("Helvetica", 12), bg="#007F5F", fg="#FFFFFF")  # White text
mail_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
mail_entry = tk.Entry(login_frame, font=("Helvetica", 12), width=25, textvariable=email_var)
add_placeholder(mail_entry, "Enter your email")  # Add the placeholder for the email field
mail_entry.grid(row=0, column=1, padx=5, pady=5)

# Label and Entry for Password
password_label = tk.Label(login_frame, text="Password:", font=("Helvetica", 12), bg="#007F5F", fg="#FFFFFF")  # White text
password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
password_entry = tk.Entry(login_frame, font=("Helvetica", 12), width=25, show="*", textvariable=password_var)
add_placeholder(password_entry, "Enter Password")  # Add the placeholder for the password field
password_entry.grid(row=1, column=1, padx=5, pady=5)

# Function to toggle password visibility
def toggle_password():
    if show_password_var.get():
        password_entry.config(show="")  # Show password
    else:
        password_entry.config(show="*")  # Hide password

# Checkbox to show/hide password
show_password_var = tk.BooleanVar()
show_password_checkbox = tk.Checkbutton(
    login_frame,
    text="Show Password",
    variable=show_password_var,
    command=toggle_password,
    font=("Helvetica", 10),
    bg="#007F5F",
)
show_password_checkbox.grid(row=2, column=1, pady=5, sticky="w")

# Function to handle login
def login():
    email = email_var.get().strip()
    password = password_var.get().strip()

    # Connect to SQLite database
    conn = sqlite3.connect("rbac_group6.db")
    cursor = conn.cursor()

    # Query to verify login credentials and check if IsActive is True
    cursor.execute("SELECT * FROM Employee WHERE Email=? AND Password=?", (email, password))
    user = cursor.fetchone()

    if user:  # Check if user exists
        if user[10] == 1:  # Assuming IsActive is the 10th column (index 9)
            employee_id = user[0]  # Assuming the first column is EmployeeID
            messagebox.showinfo("Login Successful", f"Welcome, {user[1]} {user[2]}!")  # Display welcome message

            # Insert a new log entry for the successful login
            cursor.execute("""
                INSERT INTO Log (EmployeeID, Action, Timestamp)
                VALUES (?, ?, ?)
            """, (employee_id, "Logged into the portal", sqlite3.datetime.datetime.now()))

            # Commit the changes to the database
            conn.commit()

            root.destroy()  # Close the login window
            os.system("python mainpage.py")  # Open the main page

        else:  # User found, but IsActive is not True
            messagebox.showerror("Login Failed", "Your account is inactive. Please contact an administrator.")
    
    else:  # No user found
        messagebox.showerror("Login Failed", "Invalid email or password. Please try again.")

    cursor.close()
    conn.close()

# Submit Button (Initially Disabled)
submit_button = tk.Button(
    login_frame,
    text="Submit",
    font=("Helvetica", 10, "bold"),
    bg="#002B5C",
    fg="#FFFFFF",
    state="disabled",
    command=login  # Attach the login function
)
submit_button.grid(row=3, column=1, pady=10, sticky="w")

# Run the application
root.mainloop()
