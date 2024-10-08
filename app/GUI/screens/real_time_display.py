import tkinter as tk
from tkinter import ttk
from sqlalchemy import text
from datetime import datetime
import time

from app.GUI.gui_utils import clear_screen
from app.database.order_management import check_latest_order_status
from app.database.queries import fetch_orders, update_order_status


def real_time_display(root, controller):
    clear_screen(root)
    """
    This function creates a real-time display of orders that are in 'Preparing' status.
    It updates every few seconds with new data from the database.
    """
    root.title("Restaurant Monitoring - Preparing Orders")
    root.geometry("900x600")

    # Frame for the table
    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Label at the top
    title_label = ttk.Label(frame, text="Orders in Preparation", font=("Helvetica", 18, "bold"))
    title_label.pack(pady=10)

    # Add a style for the Treeview
    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", 12))
    style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))

    # Table for displaying the orders
    columns = ("Order ID", "Customer ID", "Total Amount", "Order Time", "Delivery Address")
    table = ttk.Treeview(frame, columns=columns, show="headings", height=20)
    for col in columns:
        table.heading(col, text=col)
        table.column(col, anchor=tk.CENTER, minwidth=150, stretch=True)

    # Add a vertical scrollbar to the table
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    table.pack(fill=tk.BOTH, expand=True)

    def update_table():
        # Clear the table first
        for row in table.get_children():
            table.delete(row)

        # Update order statuses
        update_order_status()
        check_latest_order_status()

        # Fetch current orders (only 'Preparing' orders)
        orders = fetch_orders()

        # Insert fetched data into the table
        for order in orders:
            order_id, customer_id, total_amount, order_time, delivery_address = order
            formatted_time = order_time.strftime("%Y-%m-%d %H:%M:%S")
            table.insert("", tk.END,
                         values=(order_id, customer_id, f"${total_amount:.2f}", formatted_time, delivery_address))

        # Schedule the next update after 5 seconds (5000 milliseconds)
        root.after(5000, update_table)

    # Start updating the table
    update_table()

