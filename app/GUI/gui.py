import tkinter as tk
from tkinter import messagebox

from app.GUI.gui_controller import AppController

def execute_gui():


    # Create the main window
    root = tk.Tk()
    root.title("Pizza Restaurant")

    controller = AppController(root)
    # Create two buttons
    button1 = tk.Button(root, text="Log in", command=lambda: controller.show_login_screen())
    button2 = tk.Button(root, text="Create account", command=lambda: controller.show_create_account_screen())

    button1.pack(pady=10)  # pady adds padding around the button
    button2.pack(pady=10)

    # Start the main event loop
    root.mainloop()


















