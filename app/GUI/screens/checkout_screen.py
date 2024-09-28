from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox
import random
import re

from app.GUI.gui_utils import clear_screen, confirm_order
from app.database.discount_management import check_if_discount, apply_discount_code, update_discount_usage
from app.database.queries import check_if_birthday


def checkout_screen(root, order_details, controller):
    # Ensure at least one pizza is selected
    has_pizza = any(item['category'] == 'Pizza' for item in order_details)
    confirmed_discount_code = None
    code_discount = 0
    discount_id = None
    def apply_discount_and_update_total():
        nonlocal discount_label  # Allows modifying the discount_label variable from the parent scope
        nonlocal code_discount
        nonlocal confirmed_discount_code
        nonlocal discount_id  # Add this to keep track of the discount_id

        discount_code = discount_code_entry.get().strip()
        result = apply_discount_code(discount_code)

        if result is None:
            code_discount = 0  # No discount or discount already used
            discount_id = None
        else:
            code_discount, discount_id = result  # Store discount_id for later use
            code_discount = float(code_discount) * total_price  # Convert Decimal to float

        total_price_label.config(text=f"Total Price: ${total_price - code_discount - ten_orders_discount:.2f}")

        if code_discount > 0:  # Only show the discount label if there is a discount
            if discount_label is not None:
                discount_label.config(text=f"Discount: ${code_discount+ten_orders_discount:.2f}")
            else:
                discount_label = tk.Label(root, text=f"Discount: ${code_discount+ten_orders_discount:.2f}",
                                          font=("Helvetica", 12))
                discount_label.pack(pady=5)
                total_price_label.pack(pady=10)
        elif discount_label is not None:
            # If there's no discount and the label exists, remove it
            discount_label.pack_forget()
            discount_label = None  # Reset the label
    if not has_pizza:
        messagebox.showerror("Error", "You must select at least one pizza before proceeding to checkout.")
        return
    clear_screen(root)

    label = tk.Label(root, text="Checkout", font=("Helvetica", 16))
    label.pack(pady=10)

    random_postal_code = random.randint(1000, 1009)
    # Postal Code
    postal_code_label = tk.Label(root, text="Postal Code:")
    postal_code_label.pack(pady=5)
    postal_code_entry = tk.Entry(root, width=20)
    postal_code_entry.pack(pady=5)
    postal_code_entry.insert(0, str(random_postal_code))

    random_address = random.randint(1, 1000)
    # Delivery Address
    address_label = tk.Label(root, text="Delivery Address:")
    address_label.pack(pady=5)
    address_entry = tk.Entry(root, width=50)
    address_entry.pack(pady=5)
    address_entry.insert(0, str(random_address))

    # Payment Method
    payment_label = tk.Label(root, text="Payment Method:")
    payment_label.pack(pady=5)
    payment_var = tk.StringVar(value="Card")
    payment_method_frame = tk.Frame(root)
    payment_method_frame.pack(pady=5)
    tk.Radiobutton(payment_method_frame, text="Cash", variable=payment_var, value="Cash").pack(side=tk.LEFT)
    tk.Radiobutton(payment_method_frame, text="Card", variable=payment_var, value="Card").pack(side=tk.LEFT)

    # Discount Code Entry with Button
    discount_code_frame = tk.Frame(root)
    discount_code_frame.pack(pady=5)

    discount_code_label = tk.Label(discount_code_frame, text="Enter Discount Code:")
    discount_code_label.pack(side=tk.LEFT, padx=5)

    discount_code_entry = tk.Entry(discount_code_frame, width=20)
    discount_code_entry.pack(side=tk.LEFT, padx=5)

    apply_discount_button = tk.Button(discount_code_frame, text="Apply Discount Code",
                                      command=lambda: apply_discount_and_update_total())
    apply_discount_button.pack(side=tk.LEFT, padx=5)

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
    ten_orders_discount = 0
    if check_if_birthday():
        ten_orders_discount += calculate_discount(total_price)

    discount_label = None
    # Conditionally display the discount label above the total price label
    if ten_orders_discount > 0:
        discount_label = tk.Label(root, text=f"Discount: ${ten_orders_discount:.2f}", font=("Helvetica", 12))
        discount_label.pack(pady=5)

    # Display total price
    total_price_label = tk.Label(root, text=f"Total Price: ${total_price - ten_orders_discount:.2f}", font=("Helvetica", 14))
    if discount_label is not None:
        total_price_label.pack(pady=10)
    else:
        total_price_label.pack(pady=(10, 5))

        # Calculate the estimated delivery time (current time + 30 minutes)
    estimated_delivery_time = datetime.now() + timedelta(minutes=30)
    estimated_delivery_label = tk.Label(root,
                                        text=f"Estimated Delivery Time: {estimated_delivery_time.strftime('%H:%M')}",
                                        font=("Helvetica", 12))
    estimated_delivery_label.pack(pady=10)

    # Create a frame for buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Add a "Confirm Order" button
    confirm_button = tk.Button(button_frame, text="Confirm Order",
                               command=lambda: confirm_order_with_discount_update())

    confirm_button.pack(side=tk.LEFT, padx=5)

    # Add a "Back to Menu" button
    back_button = tk.Button(button_frame, text="Back to Menu", command=lambda: controller.show_main_menu_screen())
    back_button.pack(side=tk.LEFT, padx=5)

    def confirm_order_with_discount_update():
        if confirmed_discount_code:
            update_discount_usage(discount_id)
        confirm_order(root, controller, order_details, total_price - ten_orders_discount - code_discount,
                      postal_code_entry.get(), address_entry.get(), payment_var.get())

    def get_numeric_postal_code():
        # Extract only the digits from the postal code entry
        return ''.join(filter(str.isdigit, postal_code_entry.get()))

def calculate_discount(total_price):
    if check_if_discount():
        return total_price * 0.1
    return 0