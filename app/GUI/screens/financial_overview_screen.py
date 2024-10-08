import tkinter as tk
from tkinter import ttk
from app.GUI.gui_utils import clear_screen
from app.database.database import get_engine
from sqlalchemy import text
from tkcalendar import DateEntry
from datetime import datetime

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

    # Dropdown menu options
    filter_options = ["All orders", "Discounted", "Not discounted"]
    postal_code_options = [str(code) for code in range(1000, 1010)]
    age_group_options = ["All ages", "0-19", "20-29", "30-39", "40-49", "50-59", "60+"]
    gender_options = ["All genders", "Male", "Female"]

    # Lists to hold references to dropdowns
    discount_dropdowns = []
    postal_dropdowns = []
    gender_dropdowns = []

    # Age group variable
    age_group_var = tk.StringVar(value="All ages")

    def add_discount_dropdown():
        discount_var = tk.StringVar(value="All orders")
        discount_dropdown = ttk.Combobox(filter_frame, textvariable=discount_var, values=filter_options, state="readonly")
        discount_dropdown.pack(side="left", padx=10)
        discount_dropdowns.append(discount_var)

    def add_gender_dropdown():
        gender_var = tk.StringVar(value="All genders")
        gender_dropdown = ttk.Combobox(filter_frame, textvariable=gender_var, values=gender_options, state="readonly")  # Added missing comma here
        gender_dropdown.pack(side="left", padx=10)
        gender_dropdowns.append(gender_var)

    def add_postal_filter_dropdown():
        postal_var = tk.StringVar(value="All postal codes")
        postal_dropdown = ttk.Combobox(filter_frame, textvariable=postal_var, values=["All postal codes"] + postal_code_options, state="readonly")
        postal_dropdown.pack(side="left", padx=10)
        postal_dropdowns.append(postal_var)

    def add_date_filter():
        date_frame = tk.Frame(filter_frame)
        date_frame.pack(side="left", padx=10)

        start_date_label = tk.Label(date_frame, text="Start Date:")
        start_date_label.pack(side="left")

        start_date_entry = DateEntry(date_frame, width=12, background='darkblue',
                                     foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd',
                                     year=2024, month=1, day=1)
        start_date_entry.pack(side="left", padx=5)

        end_date_label = tk.Label(date_frame, text="End Date:")
        end_date_label.pack(side="left")
        end_date_entry = DateEntry(date_frame, width=12, background='darkblue',
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        end_date_entry.pack(side="left", padx=5)

        return start_date_entry, end_date_entry

    # Create date filter entries
    start_date_entry, end_date_entry = add_date_filter()

    # Add age group filter dropdown
    age_group_dropdown = ttk.Combobox(filter_frame, textvariable=age_group_var, values=age_group_options, state="readonly")
    age_group_dropdown.pack(side="left", padx=10)

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

    def calculate_age(birthdate):
        """ Calculate age from birthdate """
        today = datetime.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age

    def apply_query(frame):
        """ Query database based on the selected filters """
        query_base = """
        SELECT O.TakeAway, O.TotalAmount, O.Discount, D.delivery_postal_code, C.Birthdate, C.Gender
        FROM Orders O
        LEFT JOIN OrderDeliveries D ON O.OrderID = D.order_id
        LEFT JOIN Customer C ON O.CustomerID = C.CustomerID
        WHERE 1=1
        """

        conditions = []
        params = {}

        # Check discount dropdowns for sorting conditions
        for discount_dropdown in discount_dropdowns:
            selected_filter = discount_dropdown.get()
            if selected_filter == "Discounted":
                conditions.append("O.Discount > 0")
            elif selected_filter == "Not discounted":
                conditions.append("O.Discount = 0")

        for gender_dropdown in gender_dropdowns:
            selected_filter = gender_dropdown.get()
            if selected_filter == "Male":
                conditions.append("C.Gender = 'Male'")
            elif selected_filter == "Female":
                conditions.append("C.Gender = 'Female'")

        # Check postal code dropdowns for postal code filters
        for postal_dropdown in postal_dropdowns:
            selected_postal = postal_dropdown.get()
            if selected_postal != "All postal codes":
                conditions.append("D.delivery_postal_code = :postal_code")
                params['postal_code'] = selected_postal

        # Get date range values
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()

        # Add date conditions if specified
        if start_date:
            conditions.append("D.order_time >= :start_date")
            params['start_date'] = f"{start_date} 00:00:00"
        if end_date:
            conditions.append("D.order_time <= :end_date")
            params['end_date'] = f"{end_date} 23:59:59"

        # Filter by age group
        selected_age_group = age_group_var.get()
        if selected_age_group != "All ages":
            age_ranges = {
                "0-19": (0, 19),
                "20-29": (20, 29),
                "30-39": (30, 39),
                "40-49": (40, 49),
                "50-59": (50, 59),
                "60+": (60, 120)  # Assuming max age as 120
            }
            age_range = age_ranges[selected_age_group]
            birthdate_lower = f"DATE_SUB(CURDATE(), INTERVAL {age_range[1]} YEAR)"
            birthdate_upper = f"DATE_SUB(CURDATE(), INTERVAL {age_range[0]} YEAR)"
            conditions.append("C.Birthdate BETWEEN " + birthdate_lower + " AND " + birthdate_upper)

        # Combine conditions using AND
        if conditions:
            query_base += " AND " + " AND ".join(conditions)

        query = text(query_base)

        # Query database and get results
        with engine.connect() as connection:
            result = connection.execute(query, params)
            orders = result.fetchall()

        # Clear existing displayed orders
        clear_orders(frame)

        # Initialize total sum variable
        total_sum = 0

        if not orders:
            no_orders_label = tk.Label(frame, text="No orders found.")
            no_orders_label.pack(pady=10)
        else:
            # Display the total sum label above orders
            total_label = tk.Label(frame, text="Total Sum: $0.00", font=("Helvetica", 14, "bold"))
            total_label.pack(pady=10)

            for order in orders:
                takeaway = "Yes" if order.TakeAway else "No"
                total_amount = order.TotalAmount
                discount = order.Discount
                postal_code = order.delivery_postal_code

                order_label = tk.Label(frame,
                                       text=f"TakeAway: {takeaway}, Total: ${total_amount}, Discount: {discount}$, Postal Code: {postal_code}")
                order_label.pack(pady=5)

                total_sum += total_amount  # Accumulate total amount

            # Update the total sum label with the calculated sum
            total_label.config(text=f"Total Sum: ${total_sum:.2f}")

    # Add initial sorting dropdown
    add_discount_dropdown()
    add_gender_dropdown()
    add_postal_filter_dropdown()

    # Add mousewheel scrolling (optional)
    content_frame.bind('<Enter>', lambda e: root.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units")))
    content_frame.bind('<Leave>', lambda e: root.unbind_all("<MouseWheel>"))

    # Show all orders initially without filters applied
    apply_query(order_list_frame)

# Don't forget to include a call to the financial_overview_screen somewhere in your main application code
