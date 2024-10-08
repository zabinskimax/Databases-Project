import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from app.GUI.gui_utils import clear_screen
from app.database.queries import get_pizza_types, get_drink_types, get_desserts_types, get_ingredient_details, \
    check_if_birthday, get_pizza_ingredients, check_price_with_details, check_if_admin

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

    def show_info(food_type, category, size=None):
        if category == "Pizza":
            # Get the ingredient details, vegetarian, and vegan status
            ingredients, is_vegetarian, is_vegan = get_pizza_ingredients(food_type)

            # Get the price of the pizza based on its size
            if size:
                pizza_price, detailed_price_info = check_price_with_details(category, food_type, size, detailed=True)
            else:
                pizza_price, detailed_price_info = check_price_with_details(category, food_type,
                                                                            "Small", detailed=True)  # Default to "Small" if no size selected

            # Create the message to display
            message = f"Ingredients and Costs:\n{detailed_price_info}\n"

            if is_vegan:
                message += "This pizza is Vegan.\n"
            elif is_vegetarian:
                message += "This pizza is Vegetarian.\n"
            else:
                message += "This pizza contains non-vegetarian ingredients.\n"

            # Add the total price details
            message += f"\nTotal Price for {size or 'Small'} size: ${pizza_price:.2f}"

            # Display the information
            messagebox.showinfo("Pizza Information", message)
    def add_combobox():
        order_frame = tk.Frame(combobox_frame)
        order_frame.pack(pady=5, anchor="w")

        # Create a dictionary to hold the order details for this row
        row_order_details = {'category': None, 'item': None, 'size': None, 'price': 0.0}
        order_details.append(row_order_details)  # Add it to the global order_details list

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

        remove_button = tk.Button(order_frame, text="Remove",
                                  command=lambda: remove_combobox(order_frame, row_order_details))
        remove_button.pack(side="left", padx=5)

        def on_info_click():
            food_type = food_type_combobox.get()
            category = category_combobox.get()
            size = size_combobox.get()
            show_info(food_type, category, size)

        info_button = tk.Button(order_frame, text="Info", command=on_info_click)
        info_button.pack(side="left", padx=5)
        info_button.pack_forget()  # Initially hide the info button

        def update_price():
            selected_food = food_type_combobox.get()
            selected_size = size_combobox.get()
            category = category_combobox.get()

            if check_if_birthday():
                if category == "Pizza" and not free_pizza_applied.get():
                    item_price_float = 0.0
                    free_pizza_applied.set(True)
                elif category == "Drink" and not free_drink_applied.get():
                    item_price_float = 0.0
                    free_drink_applied.set(True)
                else:
                    item_price = check_price_with_details(category, selected_food, selected_size)
                    item_price_float = float(item_price) if item_price is not None else 0.0
            else:
                item_price = check_price_with_details(category, selected_food, selected_size)
                item_price_float = float(item_price) if item_price is not None else 0.0

            # Update the specific row in the order_details list
            row_order_details['category'] = category
            row_order_details['item'] = selected_food
            row_order_details['size'] = selected_size
            row_order_details['price'] = item_price_float

            # Update the price label in the UI
            price_label.config(text=f"Price: ${item_price_float:.2f}")

            # Recalculate the total price
            total_price.set(sum(item['price'] for item in order_details))
            total_price_label.config(text=f"Total Price: ${total_price.get():.2f}")

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
        food_type_combobox.bind('<<ComboboxSelected>>', lambda event: update_price())
        size_combobox.bind('<<ComboboxSelected>>', lambda event: update_price())

    def remove_combobox(frame, row_order_details):
        # Remove the item from the global order_details list
        order_details.remove(row_order_details)

        # Recalculate the total price based on remaining items
        total_price.set(sum(item['price'] for item in order_details))
        total_price_label.config(text=f"Total Price: ${total_price.get():.2f}")

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
    if check_if_admin():
        button3 = tk.Button(root, text="Financial overview", command=lambda: controller.show_financial_overview_screen())
        button3.pack(pady=10)
        button4 = tk.Button(root, text="Real-time display of pizzas", command=lambda: controller.show_real_time_display())
        button4.pack(pady=10)

