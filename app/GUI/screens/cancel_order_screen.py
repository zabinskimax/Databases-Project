from tkinter import messagebox

from app.GUI.gui_utils import clear_screen
import tkinter as tk

from app.database.order_management import cancel_latest_order


def cancel_order_screen(root, controller):
    clear_screen(root)

    label = tk.Label(root, text="Cancel Latest Order", font=("Helvetica", 16))
    label.pack(pady=10)

    def on_cancel_order():
        cancel_message = cancel_latest_order()
        messagebox.showinfo("Order Cancellation", cancel_message)

    cancel_order_button = tk.Button(root, text="Cancel Order", command=on_cancel_order)
    cancel_order_button.pack(pady=10)

    back_button = tk.Button(root, text="Back", command=lambda: controller.show_main_menu_screen())
    back_button.pack(pady=10)
