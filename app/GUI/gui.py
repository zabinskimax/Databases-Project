from AccountManagement.accounts import log_in, create_account

from app.GUI.screens import log_in_screen
from app.GUI.utils import log_in_button_action, create_account_button_action


def execute_gui():
    import tkinter as tk
    from tkinter import messagebox

    # Create the main window
    root = tk.Tk()
    root.title("Simple GUI with Two Buttons")


    # Create two buttons
    button1 = tk.Button(root, text="Log in", command=lambda: log_in_button_action(root))
    button2 = tk.Button(root, text="Create account", command=lambda: create_account_button_action(root))

    button1.pack(pady=10)  # pady adds padding around the button
    button2.pack(pady=10)

    # Start the main event loop
    root.mainloop()


