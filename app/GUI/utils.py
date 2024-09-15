# utils.py
from app.AccountManagement.accounts import create_account, log_in


def clear_screen(root):
    for widget in root.winfo_children():
        widget.pack_forget()

def log_in_button_action(root):
    # Import inside the function to avoid circular imports
    from app.GUI.screens import log_in_screen
    log_in_screen(root)

def create_account_button_action(root):
    from app.GUI.screens import create_accounts_screen
    create_accounts_screen(root)