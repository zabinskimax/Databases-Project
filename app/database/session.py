class Session:
    def __init__(self):
        self._customer_id = None

    def set_customer_id(self, customer_id):
        self._customer_id = customer_id

    def get_customer_id(self):
        if self._customer_id is None:
            raise ValueError("Customer ID is not set. Please log in.")
        return self._customer_id

# Singleton instance
session = Session()