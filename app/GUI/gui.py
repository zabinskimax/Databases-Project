import tkinter as tk
from tabnanny import check
from tkinter import messagebox
import tkinter.ttk as ttk

from app.database import log_in, create_account, get_pizza_types, get_drink_types, get_desserts_types, \
    get_ingredient_from_ids, get_ingredient_details, check_price, insert_order, get_pizza_id, get_drink_id, \
    get_dessert_id, check_latest_order_status, cancel_latest_order, assign_delivery, get_account_information


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

    # Main Menu Label
    label = tk.Label(root, text="Main Menu", font=("Helvetica", 16))
    label.pack(pady=10)

    # Account Information Button
    account_info_button = tk.Button(root, text="Account Information", command=lambda: account_information_screen(root))
    account_info_button.pack(anchor='ne', padx=10, pady=5)

    # Frame to hold the dynamically added comboboxes (order items)
    combobox_frame = tk.Frame(root)
    combobox_frame.pack(pady=10)

    # Define order options and their details
    order_options = ["Pizza", "Drink", "Dessert"]

    food_types = {
        "Pizza": get_pizza_types(),
        "Drink": get_drink_types(),
        "Dessert": get_desserts_types()
    }

    size_options = {
        "Pizza": ["Small", "Medium", "Large"],
        "Drink": ["Small", "Large"],
        "Dessert": []
    }

    def add_combobox():
        order_frame = tk.Frame(combobox_frame)
        order_frame.pack(pady=5, anchor="w")

        category_combobox = ttk.Combobox(order_frame, values=order_options)
        category_combobox.pack(side="left", padx=5)
        category_combobox.set("Select an order")

        food_type_combobox = ttk.Combobox(order_frame)
        food_type_combobox.pack(side="left", padx=5)
        food_type_combobox.set("")

        size_combobox = ttk.Combobox(order_frame)
        size_combobox.pack(side="left", padx=5)
        size_combobox.set("")

        remove_button = tk.Button(order_frame, text="Remove", command=lambda: remove_combobox(order_frame))
        remove_button.pack(side="left", padx=5)

        def on_category_selected(event):
            category = category_combobox.get()
            food_type_combobox['values'] = food_types.get(category, [])
            food_type_combobox.set("Select food type")
            size_combobox['values'] = size_options.get(category, [])
            size_combobox.set("")

            if category == "Dessert":
                size_combobox.pack_forget()
            else:
                size_combobox.pack(side="left", padx=5)
                size_combobox['values'] = size_options.get(category, [])
                size_combobox.set("")

        category_combobox.bind('<<ComboboxSelected>>', on_category_selected)

    def remove_combobox(frame):
        frame.destroy()

    # Button to add a new Combobox set (order item)
    add_combobox_button = tk.Button(root, text="Add an item", command=add_combobox)
    add_combobox_button.pack(pady=10)

    # Frame for the "Order" button at the bottom
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10, side="bottom")

    order_button = tk.Button(button_frame, text="Order", command=lambda: checkout_screen(root, order_details))
    order_button.pack(side="left", padx=5)

def account_information_screen(root):
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
    check_status_button = tk.Button(root, text="Check Order Status", command=lambda: check_status_screen(root))
    check_status_button.pack(pady=10)

    # Cancel Order Button
    cancel_order_button = tk.Button(root, text="Cancel an Order", command=lambda: cancel_order_screen(root))
    cancel_order_button.pack(pady=10)

    # Back to Main Menu Button
    back_button = tk.Button(root, text="Back to Menu", command=lambda: main_menu_screen(root))
    back_button.pack(pady=10)

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


def checkout_screen(root, order_details):
    # Ensure at least one pizza is selected
    has_pizza = any(item['category'] == 'Pizza' for item in order_details)

    if not has_pizza:
        messagebox.showerror("Error", "You must select at least one pizza before proceeding to checkout.")
        return
    clear_screen(root)

    label = tk.Label(root, text="Checkout", font=("Helvetica", 16))
    label.pack(pady=10)

    # Delivery Address
    address_label = tk.Label(root, text="Delivery Address:")
    address_label.pack(pady=5)
    address_entry = tk.Entry(root, width=50)
    address_entry.pack(pady=5)

    # Payment Method
    payment_label = tk.Label(root, text="Payment Method:")
    payment_label.pack(pady=5)
    payment_var = tk.StringVar(value="Card")
    payment_method_frame = tk.Frame(root)
    payment_method_frame.pack(pady=5)
    tk.Radiobutton(payment_method_frame, text="Cash", variable=payment_var, value="Cash").pack(side=tk.LEFT)
    tk.Radiobutton(payment_method_frame, text="Card", variable=payment_var, value="Card").pack(side=tk.LEFT)

    # Create a frame to hold the order details
    order_frame = tk.Frame(root)
    order_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Create a canvas and scrollbar for the order details
    canvas = tk.Canvas(order_frame)
    scrollbar = tk.Scrollbar(order_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Add order details to the scrollable frame
    total_price = 0
    for item in order_details:
        item_frame = tk.Frame(scrollable_frame)
        item_frame.pack(fill=tk.X, padx=5, pady=2)

        tk.Label(item_frame, text=f"{item['category']}:").pack(side=tk.LEFT)
        tk.Label(item_frame, text=f"{item['item']}").pack(side=tk.LEFT, padx=5)
        if item['size'] is not None:
            tk.Label(item_frame, text=f"Size: {item['size']}").pack(side=tk.LEFT, padx=5)
        tk.Label(item_frame, text=f"${item['price']:.2f}").pack(side=tk.RIGHT)

        total_price += item['price']

    # Pack the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Display total price
    total_price_label = tk.Label(root, text=f"Total Price: ${total_price:.2f}", font=("Helvetica", 14))
    total_price_label.pack(pady=10)

    # Create a frame for buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Add a "Confirm Order" button
    confirm_button = tk.Button(button_frame, text="Confirm Order",
                               command=lambda: confirm_order(root, order_details, total_price, address_entry.get(), payment_var.get()))
    confirm_button.pack(side=tk.LEFT, padx=5)

    # Add a "Back to Menu" button
    back_button = tk.Button(button_frame, text="Back to Menu", command=lambda: main_menu_screen(root))
    back_button.pack(side=tk.LEFT, padx=5)

def confirm_order(root, order_details, total_price, delivery_address, payment_method):
    # Prepare the data for insertion
    takeaway = 1  # Assuming all orders are takeaway for now
    order_status = 'Being Prepared'  # Initial status
    discount = 0  # Assuming no discount for now
    payed = 0  # Assuming not paid yet

    if not delivery_address:
        messagebox.showerror("Error", "Please enter a delivery address.")
        return

    if not payment_method:
        messagebox.showerror("Error", "Please select a payment method.")
        return

    # Insert the order into the database
    order_id = insert_order(
        takeaway,
        total_price,
        order_status,
        discount,
        payed,
        order_details,
        delivery_address,  # Pass the delivery address
        payment_method  # Pass the payment method
    )

    if order_id:
        # Assign a delivery person after the order is inserted
        designated_area = "North District"  # You might need to define how to determine the designated area
        delivery_person = assign_delivery(designated_area)

        if delivery_person:
            delivery_person_name = delivery_person.driver_name
        else:
            delivery_person_name = "No available delivery person"

        # Create the order summary
        order_summary = "Order Summary:\n\n"
        for item in order_details:
            order_summary += f"{item['category']}: {item['item']} "
            if item['size']:
                order_summary += f"(Size: {item['size']}) "
            order_summary += f"- ${item['price']:.2f}\n"

        order_summary += f"\nTotal Price: ${total_price:.2f}"
        order_summary += f"\nDelivery Address: {delivery_address}"
        order_summary += f"\nPayment Method: {payment_method}"
        order_summary += f"\nAssigned Delivery Person: {delivery_person_name}"

        messagebox.showinfo("Order Confirmed", f"Your order (ID: {order_id}) has been placed!\n\n{order_summary}")
    else:
        messagebox.showerror("Error", "There was a problem placing your order. Please try again.")

        # After confirming the order, return to the main menu
    main_menu_screen(root)

def check_status_screen(root):
    clear_screen(root)

    label = tk.Label(root, text="Check Latest Order Status", font=("Helvetica", 16))
    label.pack(pady=10)

    def on_check_status():
        status_message = check_latest_order_status()
        messagebox.showinfo("Order Status", status_message)

    check_status_button = tk.Button(root, text="Check Status", command=on_check_status)
    check_status_button.pack(pady=10)

    back_button = tk.Button(root, text="Back", command=lambda: main_menu_screen(root))
    back_button.pack(pady=10)



def cancel_order_screen(root):
    clear_screen(root)

    label = tk.Label(root, text="Cancel Latest Order", font=("Helvetica", 16))
    label.pack(pady=10)

    def on_cancel_order():
        cancel_message = cancel_latest_order()
        messagebox.showinfo("Order Cancellation", cancel_message)

    cancel_order_button = tk.Button(root, text="Cancel Order", command=on_cancel_order)
    cancel_order_button.pack(pady=10)

    back_button = tk.Button(root, text="Back", command=lambda: main_menu_screen(root))
    back_button.pack(pady=10)




