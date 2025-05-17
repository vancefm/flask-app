from flask import current_app
from data.models import db, Category
from sqlalchemy import select
from typing import List, Dict

def get_categories_with_parent_names() -> List[Dict]:
    """Returns a list of dictionaries of all Categories with parent names

    Returns:
        list(Category): A list of categories
    """
    with current_app.app_context():

        # Perform a query with joinedload to include parent relationship
        categories = Category.query.options(db.joinedload(Category.parent)).all()
        
        # Format the category names
        formatted_categories = [
            {
                'id': category.id,
                'category_name': f"{category.parent.category_name}: {category.category_name}" if category.parent else category.category_name
            }
            for category in categories
        ]
        
        sorted_categories = sorted(formatted_categories, key=lambda x: x['category_name'])
        return sorted_categories

def get_parent_id(parent_name: str) -> int | None:
    """Returns the parent id for a parent category by name

    Parent categories are the highest level categories and have no parent_ids.
    
    Args:
        name (string): A category name

    Returns:
        int: A category id

    """
    with current_app.app_context():
        result = db.session.execute(select(Category.id)
                                  .filter_by(category_name=parent_name)
                                  .filter_by(parent_id=None)).scalar_one_or_none()
        
        return result
    
def get_id_by_name_and_parent_id(name: str, parent_id: int|None) -> int | None:
    """Returns a category by name and parent id.

    Args:
        child_name (str): The child category name
        parent_id (int): The parent category id

    Returns:
        Category: A category id
    """
    with current_app.app_context():
        result = db.session.execute(
            select(Category.id)
            .filter_by(category_name=name)
            .filter_by(parent_id=parent_id)).scalar_one_or_none()
        return result

def save_category(category:Category) -> int:
    """Saves a Category to the database. If the category already exists,
    values are updated instead.

    Args:
        category (Category)

    Returns:
        _type_: The id of the object created or updated
    """
    with current_app.app_context():
        result_cat = db.session.merge(category)
        db.session.commit()
        return result_cat.id