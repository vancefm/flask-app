from datetime import datetime
from data.models.init import db
from data.models.category import Category

class Transaction(db.Model):

    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    posting_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Double, nullable=False)
    type = db.Column(db.String(15), nullable=False)
    end_balance = db.Column(db.Double, nullable=False)
    is_new = db.Column(db.Boolean, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    category = db.relationship('Category', back_populates='transactions')

    def __repr__(self):
        return f"<Transaction(id={self.id}, posting_date={self.posting_date}, "\
        f"description={self.description}, amount={self.amount}, type={self.type}, "\
        f"end_balance={self.end_balance}, is_new={self.is_new}, "\
        f"category_id={self.category_id})>"
