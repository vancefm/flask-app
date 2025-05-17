from flask import current_app
from data.models import db, CategoryPattern
from sqlalchemy import select
from typing import Dict

def get_all_category_patterns_to_dict() -> Dict:
    """
    Returns:
        dict: { CategoryPattern.id: CategoryPattern }
    """
    with current_app.app_context():    
        cgp_list = db.session.execute(select(CategoryPattern)).scalars().all()
        cgp_dict = {cgp.id: cgp for cgp in cgp_list}
        return cgp_dict
    
def get_category_pattern_from_pattern(pattern: str) -> CategoryPattern | None:
    """Get a Category Pattern from a given name

    Args:
        pattern (str): a Category Pattern name

    Returns:
        CategoryPattern | None: a Category Pattern
    """
    with current_app.app_context():
        result = db.session.execute(select(CategoryPattern)
                                  .filter_by(pattern=pattern)).scalar_one_or_none()
        return result
    
def save_category_pattern(category_pattern: CategoryPattern) -> int:
    """Save a Category Pattern to the database. If the category already exists,
    values are updated instead

    Args:
        category_pattern (CategoryPattern): A CategoryPattern

    Returns:
        int: The id of the object created or updated
    """
    with current_app.app_context():
        result_pattern = db.session.merge(category_pattern)
        db.session.commit()
        return result_pattern.id