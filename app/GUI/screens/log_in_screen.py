import tkinter as tk
from tkinter import messagebox

from app.GUI.gui_utils import clear_screen
from app.database.account_management import log_in


def log_in_screen(root, controller):
    clear_screen(root)  # Clear previous widgets
    # Create new widgets for the login screen
    label = tk.Label(root, text="Log In Screen", font=("Helvetica", 16))
    label.pack(pady=10)

    email_label = tk.Label(root, text="Email:")
    email_label.pack(pady=5)

    email_entry = tk.Entry(root)
    email_entry.pack(pady=5)
    email_entry.insert(0, "johndoe@example.com")

    password_label = tk.Label(root, text="Password:")
    password_label.pack(pady=5)

    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)
    password_entry.insert(0, "password123")

    def on_log_in():
        email = email_entry.get()
        password = password_entry.get()

        # Call the log_in function to verify credentials
        if log_in(email, password):
            messagebox.showinfo("Success", "Login successful!")
            controller.show_main_menu_screen()
        else:
            messagebox.showerror("Error", "Invalid email or password.")

    # Attach the login action without passing parameters
    login_button = tk.Button(root, text="Log In", command=on_log_in)
    login_button.pack(pady=10)

    create_account_button = tk.Button(root, text="Create Account", command=lambda: controller.show_create_account_screen())
    create_account_button.pack(pady=10)
