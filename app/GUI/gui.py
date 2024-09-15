import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

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
            main_menu_screen(root)
        else:
            messagebox.showerror("Error", "Invalid email or password.")

    # Attach the login action without passing parameters
    login_button = tk.Button(root, text="Log In", command=on_log_in)
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

    label = tk.Label(root, text="Main Menu", font=("Helvetica", 16))
    label.pack(pady=10)

    # Frame to hold the dynamically added comboboxes
    combobox_frame = tk.Frame(root)
    combobox_frame.pack(pady=10)

    # Define order options and their details
    order_options = ["Pizza", "Drinks", "Desserts"]

    food_types = {
        "Pizza": ["Margherita", "Pepperoni", "Vegetarian"],
        "Drinks": ["Coke", "Pepsi", "Water"],
        "Desserts": ["Cake", "Ice Cream", "Brownie"]
    }

    size_options = {
        "Pizza": ["Small", "Medium", "Large"],
        "Drinks": ["Small", "Medium", "Large"],
        "Desserts": ["Single", "Double", "Family"]
    }

    ingredients = {
        "Margherita":"Tomato sauce" "\n" "Mozzarella cheese" "\n" "Basil",
        "Pepperoni": "Tomato sauce" "\n" "Mozzarella cheese" "\n" "Pepperoni",
        "Vegetarian": "Tomato sauce" "\n" "Mozzarella cheese" "\n" "Assorted vegetables",
        "Coke": "Carbonated water" "\n" "Sugar" "\n" "Caffeine",
        "Pepsi": "Carbonated water" "\n" "Sugar" "\n" "Caffeine" "\n" "Flavoring",
        "Water": "Filtered water",
        "Cake": "Flour" "\n" "Sugar" "\n" "Eggs" "\n" "Butter" "\n" "Baking powder",
        "Ice Cream": "Milk" "\n" "Sugar" "\n" "Cream" "\n" "Flavoring",
        "Brownie": "Flour" "\n" "Sugar" "\n" "Cocoa powder" "\n" "Butter" "\n" "Eggs"
    }

    def on_category_selected(event, food_type_combobox, size_combobox):
        category = event.widget.get()

        # Update the food type combobox based on the selected category
        food_type_combobox['values'] = food_types.get(category, [])
        food_type_combobox.set("Select food type")

        # Clear the size combobox when a new category is selected
        size_combobox['values'] = []
        size_combobox.set("")

    def on_food_type_selected(event, category, size_combobox):
        food_type = event.widget.get()

        # Update the size combobox based on the selected category and food type
        if category in size_options:
            size_combobox['values'] = size_options[category]
            size_combobox.set("Select size")

    def show_info(food_type):
        info = ingredients.get(food_type, "No information available.")
        messagebox.showinfo("Ingredients", f"{info}")

    def add_combobox():
        # Create a new frame to hold the comboboxes for each order
        order_frame = tk.Frame(combobox_frame)
        order_frame.pack(pady=5, anchor="w")

        # Create a combobox for selecting a category (Pizza, Drinks, etc.)
        category_combobox = ttk.Combobox(order_frame, values=order_options)
        category_combobox.pack(side="left", padx=5)
        category_combobox.set("Select an order")

        # Create a combobox for selecting the food type, initially empty
        food_type_combobox = ttk.Combobox(order_frame)
        food_type_combobox.pack(side="left", padx=5)
        food_type_combobox.set("")

        # Create a combobox for selecting the size, initially empty
        size_combobox = ttk.Combobox(order_frame)
        size_combobox.pack(side="left", padx=5)
        size_combobox.set("")

        # Create a button to remove the current set of comboboxes
        remove_button = tk.Button(order_frame, text="Remove", command=lambda: remove_combobox(order_frame))
        remove_button.pack(side="left", padx=5)

        # Create a button to show information about the selected food
        info_button = tk.Button(order_frame, text="Info", command=lambda: show_info(food_type_combobox.get()))
        info_button.pack(side="left", padx=5)

        # Bind the event for selecting a category
        category_combobox.bind(
            '<<ComboboxSelected>>',
            lambda event: on_category_selected(event, food_type_combobox, size_combobox)
        )

        # Bind the event for selecting a food type to show size options
        food_type_combobox.bind(
            '<<ComboboxSelected>>',
            lambda event: on_food_type_selected(event, category_combobox.get(), size_combobox)
        )

    def remove_combobox(frame):
        frame.destroy()

    # Button to add a new Combobox set
    add_combobox_button = tk.Button(root, text="Add an item", command=add_combobox)
    add_combobox_button.pack(pady=10)

    # Frame for the "Back" and "Order" buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10, side="bottom")

    # Back button
    back_button = tk.Button(button_frame, text="Back", command=lambda: log_in_screen(root))
    back_button.pack(side="left", padx=5)

    # Non-functional "Order" button
    order_button = tk.Button(button_frame, text="Order")
    order_button.pack(side="left", padx=5)

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




