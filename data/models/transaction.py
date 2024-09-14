from datetime import datetime
from data.models import db
from decimal import Decimal, ROUND_DOWN

class Transaction(db.Model):

    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    posting_date = db.Column(db.Integer, nullable=False) # Epoch time
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    type = db.Column(db.String(15), nullable=False)
    end_balance = db.Column(db.Numeric(10,2), nullable=False)
    is_new = db.Column(db.Boolean, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    # Define relationships to other tables
    tx_category = db.relationship('Category', back_populates='ctg_transaction')

    def __init__(self, posting_date, description, amount, type, end_balance, is_new, category_id):
        self.posting_date = posting_date
        self.description = description
        self.amount = amount
        self.type = type
        self.end_balance = end_balance
        self.is_new = is_new
        self.category_id = category_id

    def __repr__(self):
        return f"<Transaction(id={self.id}, posting_date={self.posting_date}, "\
        f"description={self.description}, amount={self.amount}, type={self.type}, "\
        f"end_balance={self.end_balance}, is_new={self.is_new}, "\
        f"category_id={self.category_id})>"

    @property
    def posting_date_as_epoch_timestamp(self):
        """
        Returns:
            datetime: The converted datetime format of the transaction's integer posting date

        Example: YYYY-MM-DD hh-mm-ss
        """
        return datetime.fromtimestamp(self.posting_date)
    
    @posting_date_as_epoch_timestamp.setter
    def posting_date_as_datetime(self, ts_value: datetime):
        """A setter method that converts a datetime value to and integer
        posting date.

        Args:
            ts_value (datetime): A datetime posting date

        Example: transaction.posting_date_as_datetime = datetime(2024,1,1,12,0,0)
        """
        self.posting_date = int(ts_value.timestamp())