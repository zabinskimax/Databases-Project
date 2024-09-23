from tkinter import messagebox
import tkinter as tk

from app.GUI.gui_utils import clear_screen
from app.database.queries import get_account_information


def account_information_screen(root, controller):
    clear_screen(root)

    # Fetch account information from the database
    account_info = get_account_information()

    if not account_info:
        messagebox.showerror("Error", "Unable to fetch account information.")
        return

    # Account Information Label
    label = tk.Label(root, text="Account Information", font=("Helvetica", 16))
    label.pack(pady=10)

    # Display Account Information
    info_labels = [
        ("Name:", account_info['Name']),
        ("Gender:", account_info['Gender']),
        ("Birthdate:", account_info['Birthdate']),
        ("Phone Number:", account_info['PhoneNumber']),
        ("Address:", account_info['Address']),
        ("Email:", account_info['Email']),
        ("Number of Orders:", account_info['NumberOfOrders']),
    ]

    for label_text, value in info_labels:
        info_label = tk.Label(root, text=f"{label_text} {value}", font=("Helvetica", 12))
        info_label.pack(pady=5)

    # Check Order Status Button
    check_status_button = tk.Button(root, text="Check Order Status", command=lambda: controller.show_check_status_screen())
    check_status_button.pack(pady=10)

    # Cancel Order Button
    cancel_order_button = tk.Button(root, text="Cancel an Order", command=lambda: controller.show_cancel_order_screen())
    cancel_order_button.pack(pady=10)

    # Back to Main Menu Button
    back_button = tk.Button(root, text="Back to Menu", command=lambda: controller.show_main_menu_screen())
    back_button.pack(pady=10)