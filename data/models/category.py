from data.models import db
from sqlalchemy.schema import UniqueConstraint

class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(25), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    # Define self-referential relationship between parent_id and id fields
    parent = db.relationship('Category', remote_side=[id], back_populates='children')
    children = db.relationship('Category', back_populates='parent', remote_side=[parent_id])

    # Define relationships to other tables
    ctg_transaction = db.relationship('Transaction', back_populates='tx_category')
    ctg_category_pattern = db.relationship('CategoryPattern', back_populates='cptrn_category')

    # Unique constraint for category_name:parent_id combo
    __table_args__ = (UniqueConstraint('category_name', 'parent_id', name='_category_parent_uc'),)

    def __init__(self, category_name, parent_id=None):
        self.category_name = category_name
        self.parent_id = parent_id

    def __repr__(self):
        return f"<Category(id={self.id}, "\
            f"category_name='{self.category_name}', "\
            f"parent_id={self.parent_id})>" 