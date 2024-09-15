from data.models import db
from sqlalchemy.schema import UniqueConstraint

class CategoryPattern(db.Model):

    __tablename__ = 'category_patterns'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    pattern = db.Column(db.String(100), nullable=False, unique=True)

    # Define relationships to other tables
    cptrn_category = db.relationship('Category', back_populates='ctg_category_pattern')

    def __init__(self, category_id, pattern):
        self.category_id = category_id
        self.pattern = pattern 

    def __repr__(self):
        return f"<CategoryPattern(id={self.id}, category_id='{self.category_id}', "\
            f"pattern={self.pattern})>"