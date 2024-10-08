import tkinter as tk
from tkinter import ttk  # Import ttk for Combobox
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar
from app.GUI.gui_utils import clear_screen
from app.database.account_management import create_account


def create_accounts_screen(root, controller):
    clear_screen(root)  # Clear previous widgets

    label = tk.Label(root, text="Create Account Screen", font=("Helvetica", 16))
    label.pack(pady=10)

    global name_entry, gender_combobox, birthdate_entry, phone_entry, address_entry, email_entry, password_entry, number_of_orders_entry
    name_entry = tk.Entry(root)

    # Change gender to a Combobox
    gender_combobox = ttk.Combobox(root, values=["male", "female"])  # Combobox for gender options
    gender_combobox.set("male")  # Set default value

    # Replace birthdate_entry with a DateEntry from tkcalendar
    birthdate_entry = DateEntry(root, date_pattern='yyyy-mm-dd')  # Specify date format
    phone_entry = tk.Entry(root)
    address_entry = tk.Entry(root)
    email_entry = tk.Entry(root)
    password_entry = tk.Entry(root, show="*")

    # Set default values
    name_entry.insert(0, "John Doe")
    phone_entry.insert(0, "1234567890")
    address_entry.insert(0, "123 Main St")
    email_entry.insert(0, "johndoe@example.com")
    password_entry.insert(0, "password123")

    labels = ["Name", "Gender", "Birthdate", "Phone Number", "Address", "Email", "Password", "Number of Orders"]
    entries = [name_entry, gender_combobox, birthdate_entry, phone_entry, address_entry, email_entry, password_entry]

    for label_text, entry in zip(labels, entries):
        tk.Label(root, text=label_text).pack(pady=5)
        entry.pack(pady=5)

    def on_create_account():
        create_account(
            name_entry.get(),
            gender_combobox.get(),  # Get selected gender from the combobox
            birthdate_entry.get(),  # Get selected birthdate
            phone_entry.get(),
            address_entry.get(),
            email_entry.get(),
            password_entry.get(),
            0
        )
        controller.show_login_screen()

    create_account_button = tk.Button(root, text="Create Account", command=on_create_account)
    create_account_button.pack(pady=10)

    back_to_login_button = tk.Button(root, text="Back to Log In", command=lambda: controller.show_login_screen())
    back_to_login_button.pack(pady=10)
