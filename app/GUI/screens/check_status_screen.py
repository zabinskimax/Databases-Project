from tkinter import messagebox
import tkinter as tk

from app.GUI.gui_utils import clear_screen
from app.database.order_management import check_latest_order_status


def check_status_screen(root, controller):
    clear_screen(root)

    label = tk.Label(root, text="Check Latest Order Status", font=("Helvetica", 16))
    label.pack(pady=10)

    def on_check_status():
        status_message = check_latest_order_status()
        messagebox.showinfo("Order Status", status_message)

    check_status_button = tk.Button(root, text="Check Status", command=on_check_status)
    check_status_button.pack(pady=10)

    back_button = tk.Button(root, text="Back", command=lambda: controller.show_main_menu_screen())
    back_button.pack(pady=10)
