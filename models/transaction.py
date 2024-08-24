

class Transaction:

    def __init__(self, posting_date, description, amount, type, end_balance, other_details=None):
        self.posting_date = posting_date
        self.description = description
        self.amount = amount
        self.type = type
        self.end_balance = end_balance
        self.other_details = other_details