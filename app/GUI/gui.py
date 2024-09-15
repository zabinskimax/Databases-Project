import tkinter as tk

from app.database import log_in, create_account


def execute_gui():

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

def clear_screen(root):
    for widget in root.winfo_children():
        widget.pack_forget()


def log_in_button_action(root):
    log_in_screen(root)

def create_account_button_action(root):
    create_accounts_screen(root)

def log_in_screen(root):
    clear_screen(root)  # Clear previous widgets
    # Create new widgets for the login screen
    label = tk.Label(root, text="Log In Screen", font=("Helvetica", 16))
    label.pack(pady=10)

    email_label = tk.Label(root, text="Email:")
    email_label.pack(pady=5)

    email_entry = tk.Entry(root)
    email_entry.pack(pady=5)

    password_label = tk.Label(root, text="Password:")
    password_label.pack(pady=5)

    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    login_button = tk.Button(root, text="Log In", command=lambda: log_in(email_entry.get(), password_entry.get()))
    login_button.pack(pady=10)

    create_account_button = tk.Button(root, text="Create Account", command=lambda: create_account_button_action(root))
    create_account_button.pack(pady=10)

def create_accounts_screen(root):
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
        main_menu_screen(root)

    create_account_button = tk.Button(root, text="Create Account", command=on_create_account)
    create_account_button.pack(pady=10)

    back_to_login_button = tk.Button(root, text="Back to Log In", command=lambda: log_in_screen(root))
    back_to_login_button.pack(pady=10)



def main_menu_screen(root):
    clear_screen(root)
    label = tk.Label(root, text="Log In Screen", font=("Helvetica", 16))
    label.pack(pady=10)

    take_order_button = tk.Button(root, text="Log In", command=take_order_screen)
    take_order_button.pack(pady=10)

def take_order_screen(root):
    clear_screen(root)
    username_label = tk.Label(root, text="Username:")
    username_label.pack(pady=5)
    username_label = tk.Label(root, text="Username:")
    username_label.pack(pady=5)
    username_label = tk.Label(root, text="Username:")
    username_label.pack(pady=5)
    username_label = tk.Label(root, text="Username:")
    username_label.pack(pady=5)




