from data.models.init import db

class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(25), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    parent = db.relationship('Category', remote_side=[id], back_populates='children')
    children = db.relationship('Category', back_populates='parent', remote_side=[parent])

    transactions = db.relationship('Transaction', back_populates='category')
    category_patterns = db.relationship('CategoryPattern', back_populates='category_patterns')

    def __repr__(self):
        return f"<Category(id={self.id}, category_name='{self.category_name}', parent_id={self.parent_id})>"