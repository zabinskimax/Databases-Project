import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from app.GUI.gui_utils import clear_screen
from app.database.queries import get_pizza_types, get_drink_types, get_desserts_types, get_ingredient_details, check_price, check_if_birthday

# Track if the free pizza and drink have been applied
free_pizza_applied = tk.BooleanVar(value=False)
free_drink_applied = tk.BooleanVar(value=False)


def main_menu_screen(root, controller):
    clear_screen(root)

    # Main Menu Label
    label = tk.Label(root, text="Main Menu", font=("Helvetica", 16))
    label.pack(pady=10)

    # Account Information Button
    account_info_button = tk.Button(root, text="Account Information", command=lambda: controller.show_account_information_screen())
    account_info_button.pack(anchor='ne', padx=10, pady=5)

    # Check if it's the customer's birthday
    if check_if_birthday():
        birthday_message = tk.Label(root, text="Happy Birthday! You get a free pizza and drink!",
                                    font=("Helvetica", 14), fg="green")
        birthday_message.pack(pady=10)

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
    # Variable to store the total price
    total_price = tk.DoubleVar()
    total_price.set(0.00)

    # List to store order details
    order_details = []
    # Label to display the total price
    total_price_label = tk.Label(root, text="Total Price: $0.00", font=("Helvetica", 14))
    total_price_label.pack(pady=10)

    def on_food_type_selected(event, category, size_combobox):
        food_type = event.widget.get()

        # Update the size combobox based on the selected category and food type
        if category in size_options:
            size_combobox['values'] = size_options[category]
            size_combobox.set("Select size")

    def show_info(food_type, category):
        if category == "Pizza":
            ingredients = get_ingredient_details(food_type, category)

            messagebox.showinfo("Ingredient Information", ingredients)
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

        price_label = tk.Label(order_frame, text="Price: $0.00", width=12)
        price_label.pack(side="left", padx=5)

        remove_button = tk.Button(order_frame, text="Remove", command=lambda: remove_combobox(order_frame))
        remove_button.pack(side="left", padx=5)

        def on_info_click():
            food_type = food_type_combobox.get()
            category = category_combobox.get()
            show_info(food_type, category)

        info_button = tk.Button(order_frame, text="Info", command=on_info_click)
        info_button.pack(side="left", padx=5)
        info_button.pack_forget()  # Initially hide the info button
        def update_price_for_desserts():
            if category_combobox.get()== 'Dessert':
                update_price()
        def update_price():
            selected_food = food_type_combobox.get()
            selected_size = size_combobox.get()
            category = category_combobox.get()
            # Check if the customer is eligible for a free pizza or drink
            if check_if_birthday():
                if category == "Pizza" and not free_pizza_applied.get():
                    item_price_float = 0.0
                    free_pizza_applied.set(True)
                elif category == "Drink" and not free_drink_applied.get():
                    item_price_float = 0.0
                    free_drink_applied.set(True)
                else:
                    item_price = check_price(category, selected_food, selected_size)
                    item_price_float = float(item_price) if item_price is not None else 0.0
            else:
                item_price = check_price(category, selected_food, selected_size)
                item_price_float = float(item_price) if item_price is not None else 0.0

                # Check if this item is already in the order
                existing_item = next(
                    (item for item in order_details if item['category'] == category and item['item'] == selected_food),
                    None)

                if existing_item:
                    # If the item already exists, update its price and size
                    current_total = total_price.get()
                    current_total -= existing_item['price']  # Subtract the old price
                    new_total = current_total + item_price_float  # Add the new price
                    total_price.set(new_total)
                    total_price_label.config(text=f"Total Price: ${new_total:.2f}")

                    existing_item['size'] = selected_size
                    existing_item['price'] = item_price_float
                else:
                    # If the item is new, add it to the order
                    current_total = total_price.get()
                    new_total = current_total + item_price_float
                    total_price.set(new_total)
                    total_price_label.config(text=f"Total Price: ${new_total:.2f}")

                    order_details.append({
                        'category': category,
                        'item': selected_food,
                        'size': selected_size,
                        'price': item_price_float
                    })
                price_label.config(text=f"Price: ${item_price_float:.2f}")

        def on_category_selected(event):
            category = category_combobox.get()
            food_type_combobox['values'] = food_types.get(category, [])
            food_type_combobox.set("Select food type")
            size_combobox['values'] = size_options.get(category, [])
            size_combobox.set("")
            if category == "Pizza":
                info_button.pack(side="left", padx=5)
            else:
                info_button.pack_forget()
            if category == "Dessert":
                size_combobox.pack_forget()
            else:
                size_combobox.pack(side="left", padx=5)
                size_combobox['values'] = size_options.get(category, [])
                size_combobox.set("")

        category_combobox.bind('<<ComboboxSelected>>', on_category_selected)

        food_type_combobox.bind('<<ComboboxSelected>>', lambda event: update_price_for_desserts())
        size_combobox.bind('<<ComboboxSelected>>', lambda event: update_price())

    def remove_combobox(frame):
        # Get the price of the item being removed
        price_label = frame.winfo_children()[3]  # Assuming the price label is the 4th child of the frame
        item_price = float(price_label.cget("text").split("$")[1])

        # Update total price
        current_total = total_price.get()
        new_total = current_total - item_price
        total_price.set(new_total)
        total_price_label.config(text=f"Total Price: ${new_total:.2f}")

        # Remove the item from order details
        for item in order_details:
            if item['price'] == item_price:
                order_details.remove(item)
                break

        frame.destroy()

    # Button to add a new Combobox set (order item)
    add_combobox_button = tk.Button(root, text="Add an item", command=add_combobox)
    add_combobox_button.pack(pady=10)

    # Frame for the "Order" button at the bottom
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10, side="bottom")

    order_button = tk.Button(button_frame, text="Order", command=lambda: controller.show_checkout_screen(order_details))
    order_button.pack(side="left", padx=5)

    # Back button
    back_button = tk.Button(button_frame, text="Back", command=lambda: controller.show_login_screen())
    back_button.pack(side="left", padx=5)


