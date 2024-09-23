import tkinter as tk

from app.GUI.gui_utils import clear_screen
from app.database.account_management import create_account


def create_accounts_screen(root, controller):
    clear_screen(root)  # Clear previous widgets

    label = tk.Label(root, text="Create Account Screen", font=("Helvetica", 16))
    label.pack(pady=10)

    global name_entry, gender_entry, birthdate_entry, phone_entry, address_entry, email_entry, password_entry, number_of_orders_entry
    name_entry = tk.Entry(root)
    gender_entry = tk.Entry(root)
    birthdate_entry = tk.Entry(root)
    phone_entry = tk.Entry(root)
    address_entry = tk.Entry(root)
    email_entry = tk.Entry(root)
    password_entry = tk.Entry(root, show="*")
    number_of_orders_entry = tk.Entry(root)

    # Set default values
    name_entry.insert(0, "John Doe")
    gender_entry.insert(0, "male")
    birthdate_entry.insert(0, "1990-01-01")
    phone_entry.insert(0, "1234567890")
    address_entry.insert(0, "123 Main St")
    email_entry.insert(0, "johndoe@example.com")
    password_entry.insert(0, "password123")
    number_of_orders_entry.insert(0, "0")

    labels = ["Name", "Gender", "Birthdate (YYYY-MM-DD)", "Phone Number", "Address", "Email", "Password", "Number of Orders"]
    entries = [name_entry, gender_entry, birthdate_entry, phone_entry, address_entry, email_entry, password_entry, number_of_orders_entry]

    for label_text, entry in zip(labels, entries):
        tk.Label(root, text=label_text).pack(pady=5)
        entry.pack(pady=5)

    def on_create_account():
        create_account(
            name_entry.get(),
            gender_entry.get(),
            birthdate_entry.get(),
            phone_entry.get(),
            address_entry.get(),
            email_entry.get(),
            password_entry.get(),
            number_of_orders_entry.get()
        )
        controller.show_main_menu_screen()

    create_account_button = tk.Button(root, text="Create Account", command=on_create_account)
    create_account_button.pack(pady=10)

    back_to_login_button = tk.Button(root, text="Back to Log In", command=lambda: controller.show_login_screen())
    back_to_login_button.pack(pady=10)

