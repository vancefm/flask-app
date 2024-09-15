from flask import current_app
from data.models import db, CategoryPattern
from sqlalchemy import select

def get_all_category_patterns_to_dict():
    with current_app.app_context():    
        cgp_list = db.session.execute(select(CategoryPattern)).scalars().all()
        cgp_dict = {cgp.id: cgp for cgp in cgp_list}
        return cgp_dict
    
def get_category_pattern_from_pattern(pattern: str):
    with current_app.app_context():
        result = db.session.execute(select(CategoryPattern)
                                  .where(CategoryPattern.pattern == pattern)).fetchone()
        return result
    
def save_category_pattern(category_pattern: CategoryPattern):
    with current_app.app_context():
        db.session.add(category_pattern)
        return db.session.commit()