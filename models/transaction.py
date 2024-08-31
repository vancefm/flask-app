

class Transaction:

    def __init__(self, posting_date, description, amount, type, end_balance,
                 is_new=True, category_name="Uncategorized"):
        self.posting_date = posting_date
        self.description = description
        self.amount = amount
        self.type = type
        self.end_balance = end_balance
        self.is_new = is_new
        self.category_name = category_name
        
    def __repr__(self):
        return f"Transaction({self.posting_date}, {self.description}, {self.amount}, " \
            f"{self.type}, {self.end_balance}, {self.is_new}, {self.category_name})"