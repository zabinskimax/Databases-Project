import tkinter as tk
from tkinter import messagebox


from app.GUI.gui_utils import clear_screen, confirm_order


def checkout_screen(root, order_details, controller):
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
                               command=lambda: confirm_order(root, controller, order_details, total_price, address_entry.get(), payment_var.get()))
    confirm_button.pack(side=tk.LEFT, padx=5)

    # Add a "Back to Menu" button
    back_button = tk.Button(button_frame, text="Back to Menu", command=lambda: controller.show_main_menu_screen(root))
    back_button.pack(side=tk.LEFT, padx=5)