import tkinter as tk

from app.AccountManagement.accounts import create_account, log_in
from app.GUI.utils import clear_screen, create_account_button_action


def log_in_screen(root):
    from app.GUI.utils import clear_screen, create_account_button_action
    clear_screen(root)  # Clear previous widgets
    # Create new widgets for the login screen
    label = tk.Label(root, text="Log In Screen", font=("Helvetica", 16))
    label.pack(pady=10)

    username_label = tk.Label(root, text="Username:")
    username_label.pack(pady=5)

    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    password_label = tk.Label(root, text="Password:")
    password_label.pack(pady=5)

    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    login_button = tk.Button(root, text="Log In", command=log_in)
    login_button.pack(pady=10)

    create_account_button = tk.Button(root, text="Create Account", command=lambda: create_account_button_action(root))
    create_account_button.pack(pady=10)

def create_accounts_screen(root):
    from app.GUI.utils import clear_screen
    clear_screen(root)  # Clear previous widgets

    # Create new widgets for the create account screen
    label = tk.Label(root, text="Create Account Screen", font=("Helvetica", 16))
    label.pack(pady=10)

    new_username_label = tk.Label(root, text="New Username:")
    new_username_label.pack(pady=5)

    new_username_entry = tk.Entry(root)
    new_username_entry.pack(pady=5)

    new_password_label = tk.Label(root, text="New Password:")
    new_password_label.pack(pady=5)

    new_password_entry = tk.Entry(root, show="*")
    new_password_entry.pack(pady=5)

    create_account_button = tk.Button(root, text="Create Account",
                                      command= create_account)
    create_account_button.pack(pady=10)

    back_to_login_button = tk.Button(root, text="Back to Log In", command=lambda: log_in_screen(root))
    back_to_login_button.pack(pady=10)