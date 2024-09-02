from data.models.init import db

class CategoryPattern(db.Model):

    __tablename__ = 'category_patterns'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    pattern = db.Column(db.String(100), nullable=False)

    category = db.relationship('Category', back_populates='categories')

    def __repr__(self):
        return f"<Category(id={self.id}, category_id='{self.category_id}', "\
            f"pattern={self.pattern})>"