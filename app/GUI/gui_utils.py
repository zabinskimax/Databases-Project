from tkinter import messagebox

from app.database.delivery_management import assign_delivery
from app.database.order_management import insert_order


def clear_screen(root):
    for widget in root.winfo_children():
        widget.pack_forget()

def confirm_order(root, controller, order_details, total_price, delivery_postal_code, delivery_address, payment_method):
    # Prepare the data for insertion
    takeaway = 1  # Assuming all orders are takeaway for now
    order_status = 'Preparing'  # Initial status
    discount = 0  # Assuming no discount for now
    payed = 0  # Assuming not paid yet

    if not delivery_postal_code:
        messagebox.showerror("Error", "Please enter a delivery postal code.")
        return

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
        delivery_postal_code,
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
        order_summary += f"\nDelivery Postal Code: {delivery_postal_code}"
        order_summary += f"\nDelivery Address: {delivery_address}"
        order_summary += f"\nPayment Method: {payment_method}"
        order_summary += f"\nAssigned Delivery Person: {delivery_person_name}"

        messagebox.showinfo("Order Confirmed", f"Your order (ID: {order_id}) has been placed!\n\n{order_summary}")
    else:
        messagebox.showerror("Error", "There was a problem placing your order. Please try again.")

        # After confirming the order, return to the main menu
    controller.show_main_menu_screen()

