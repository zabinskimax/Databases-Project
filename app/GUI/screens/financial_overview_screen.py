import tkinter as tk
from tkinter import ttk
from app.GUI.gui_utils import clear_screen
from app.database.database import get_engine
from sqlalchemy import text

# Assuming the engine is correctly set up for your database
engine = get_engine()

def financial_overview_screen(root, controller):
    clear_screen(root)

    # Create a frame to contain the canvas and scrollbar
    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    # Create a canvas
    canvas = tk.Canvas(container)
    canvas.pack(side="left", fill="both", expand=True)

    # Add a scrollbar to the canvas
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure canvas to respond to the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Create another frame inside the canvas to hold the content
    content_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    # Title label
    label = tk.Label(content_frame, text="Financial Overview", font=("Helvetica", 16))
    label.pack(pady=10)

    # Filter section frame
    filter_frame = tk.Frame(content_frame)
    filter_frame.pack(pady=10, fill="x")

    # Initial sorting options
    filter_options = ["All orders", "Discounted", "Takeaway", "Received in person"]
    filter_options_postal = ["All postal codes", "North", "South", "East", "West"]

    # Lists to hold references to dropdowns
    dropdowns = []  # For order filters
    postal_dropdowns = []  # For postal code filters

    # Function to add a new sorting dropdown
    def add_filter_dropdown():
        dropdown = ttk.Combobox(filter_frame, values=filter_options)
        dropdown.current(0)  # Default to "All orders"
        dropdown.pack(side="left", padx=5)
        dropdowns.append(dropdown)  # Store reference for removal
        update_apply_button_state()  # Update button state

    # Function to add a new postal code dropdown
    def add_postal_filter_dropdown():
        dropdown = ttk.Combobox(filter_frame, values=filter_options_postal)
        dropdown.current(0)  # Default to "All postal codes"
        dropdown.pack(side="left", padx=5)
        postal_dropdowns.append(dropdown)  # Store reference for removal
        update_apply_button_state()  # Update button state

    # Function to remove the last sorting dropdown
    def remove_filter_dropdown():
        if dropdowns:
            dropdowns[-1].destroy()  # Remove the last dropdown
            dropdowns.pop()  # Remove from the list
            update_apply_button_state()  # Update button state

    # Function to remove the last postal filter dropdown
    def remove_postal_filter_dropdown():
        if postal_dropdowns:
            postal_dropdowns[-1].destroy()  # Remove the last postal dropdown
            postal_dropdowns.pop()  # Remove from the list
            update_apply_button_state()  # Update button state

    # Button to add a sorting dropdown
    add_button = tk.Button(filter_frame, text="Add order filter", command=add_filter_dropdown)
    add_button.pack(side="right", padx=5)

    # Button to add a postal filter dropdown
    add_postal_button = tk.Button(filter_frame, text="Add postal filter", command=add_postal_filter_dropdown)
    add_postal_button.pack(side="right", padx=5)

    # Button to remove a sorting dropdown
    remove_button = tk.Button(filter_frame, text="Remove filter", command=remove_filter_dropdown)
    remove_button.pack(side="right", padx=5)

    # Button to remove a postal filter dropdown
    remove_postal_button = tk.Button(filter_frame, text="Remove postal filter", command=remove_postal_filter_dropdown)
    remove_postal_button.pack(side="right", padx=5)

    # Button to apply the filters
    def apply_filters():
        clear_orders(order_list_frame)  # Clear existing orders before showing filtered ones
        apply_query(order_list_frame)

    apply_button = tk.Button(filter_frame, text="Apply Filter", command=apply_filters)
    apply_button.pack(side="right", padx=10)

    # Placeholder for where the orders will be displayed
    order_list_frame = tk.Frame(content_frame)
    order_list_frame.pack(pady=10, fill="x")

    def clear_orders(frame):
        """ Clear existing displayed orders """
        for widget in frame.winfo_children():
            widget.destroy()

    def apply_query(frame):
        """ Query database based on the selected filters """
        query_base = "SELECT TakeAway, TotalAmount, Discount FROM Orders WHERE 1=1"
        conditions = []
        params = {}

        # Check each dropdown for sorting conditions
        for dropdown in dropdowns:
            selected_filter = dropdown.get()
            if selected_filter == "Discounted":
                conditions.append("Discount > 0")
            elif selected_filter == "Takeaway":
                conditions.append("TakeAway = :takeaway")
                params['takeaway'] = 1  # TakeAway is 1 for Yes
            elif selected_filter == "Received in person":
                conditions.append("TakeAway = :takeaway")
                params['takeaway'] = 0  # TakeAway is 0 for No

        # Check postal dropdowns for postal conditions
        for postal_dropdown in postal_dropdowns:
            selected_postal_filter = postal_dropdown.get()
            if selected_postal_filter == "North":
                conditions.append("PostalCode IN (SELECT PostalCode FROM PostalRegions WHERE Region = 'North')")
            elif selected_postal_filter == "South":
                conditions.append("PostalCode IN (SELECT PostalCode FROM PostalRegions WHERE Region = 'South')")
            elif selected_postal_filter == "East":
                conditions.append("PostalCode IN (SELECT PostalCode FROM PostalRegions WHERE Region = 'East')")
            elif selected_postal_filter == "West":
                conditions.append("PostalCode IN (SELECT PostalCode FROM PostalRegions WHERE Region = 'West')")

        # Combine conditions using AND
        if conditions:
            query_base += " AND " + " AND ".join(conditions)  # Use AND to combine conditions

        query = text(query_base)

        # Query database and get results
        with engine.connect() as connection:
            result = connection.execute(query, params)
            orders = result.fetchall()

        # Display orders based on query result
        clear_orders(frame)  # Clear existing displayed orders
        if not orders:
            no_orders_label = tk.Label(frame, text="No orders found.")
            no_orders_label.pack(pady=10)
        else:
            for order in orders:
                takeaway = "Yes" if order.TakeAway else "No"
                total_amount = order.TotalAmount
                discount = order.Discount

                order_label = tk.Label(frame,
                                       text=f"TakeAway: {takeaway}, Total: ${total_amount}, Discount: {discount}%")
                order_label.pack(pady=5)

    def update_apply_button_state():
        """ Enable or disable the apply button based on the presence of dropdowns """
        apply_button.config(state=tk.NORMAL if dropdowns or postal_dropdowns else tk.DISABLED)

    # Add initial sorting dropdown
    add_filter_dropdown()  # Start with one order dropdown
    add_postal_filter_dropdown()  # Start with one postal dropdown

    # Add mousewheel scrolling (optional)
    content_frame.bind('<Enter>', lambda e: root.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units")))
    content_frame.bind('<Leave>', lambda e: root.unbind_all("<MouseWheel>"))

    # Show all orders initially without filters applied
    apply_query(order_list_frame)
