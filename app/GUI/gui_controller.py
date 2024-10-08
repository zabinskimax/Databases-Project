# app/gui/gui_controller.py
from app.GUI.screens.real_time_display import real_time_display


class AppController:
    def __init__(self, root):
        self.root = root

    def show_login_screen(self):
        from app.GUI.screens.log_in_screen import log_in_screen
        log_in_screen(self.root, self)

    def show_create_account_screen(self):
        from app.GUI.screens.create_account_screen import create_accounts_screen
        create_accounts_screen(self.root, self)

    def show_main_menu_screen(self):
        from app.GUI.screens.main_menu_screen import main_menu_screen
        main_menu_screen(self.root, self)

    def show_account_information_screen(self):
        from app.GUI.screens.account_information_screen import account_information_screen
        account_information_screen(self.root, self)

    def show_check_status_screen(self):
        from app.GUI.screens.check_status_screen import check_status_screen
        check_status_screen(self.root, self)

    def show_cancel_order_screen(self):
        from app.GUI.screens.cancel_order_screen import cancel_order_screen
        cancel_order_screen(self.root, self)

    def show_take_order_screen(self):
        from app.GUI.screens.take_order_screen import take_order_screen
        take_order_screen(self.root, self)

    def show_checkout_screen(self, order_details):
        from app.GUI.screens.checkout_screen import checkout_screen
        checkout_screen(self.root, order_details, self)

    def show_financial_overview_screen(self):
        from app.GUI.screens.financial_overview_screen import financial_overview_screen
        financial_overview_screen(self.root, self)

    def show_real_time_display(self):
        from app.GUI.screens.real_time_display import real_time_display
        real_time_display(self.root, self)