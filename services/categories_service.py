from flask import current_app
from data.models import db, Category
from sqlalchemy import select

def get_all_categories_to_dict():
    with current_app.app_context():    
        cg_list = db.session.execute(select(Category)).scalars().all()
        cg_dict = {cg.id: cg for cg in cg_list}
        return cg_dict 


def get_parent_by_name(name: str):
    """Returns a parent category by name.

    Parent categories are the highest level categories and have no parent_ids.

    Args:
        name (string): A category name

    Returns:
        Category: A parent category
    """
    with current_app.app_context():
        result = db.session.execute(select(Category)
                                .where(Category.category_name == name)
                                .where(Category.parent_id == None)).fetchone()
        return result[0] if result else None

def get_parent_id_from_parent_name(parent_name: str):
    """Returns the parent id for a parent category by name

    Parent categories are the highest level categories and have no parent_ids.
    
    Args:
        name (string): A category name

    Returns:
        int: category id

    """
    with current_app.app_context():
        result = db.session.execute(select(Category.id)
                                  .where(Category.category_name == parent_name)
                                  .where(Category.parent_id == None)).fetchone()
        return result[0] if result else None
    
def get_id_by_name_and_parent_id(name: str, parent_id: int):
    """Returns a category by name and parent id.

    Args:
        child_name (str): The child category name
        parent_id (int): The parent category id

    Returns:
        Category: A category
    """
    with current_app.app_context():
        result = db.session.execute(select(Category.id)
                                  .where(Category.category_name == name)
                                  .where(Category.parent_id == parent_id)).fetchone()
        return result[0] if result else None

def save_category(category:Category):
    """Saves a Category to the database

    Args:
        category (Category)

    Returns:
        _type_: _description_
    """
    with current_app.app_context():
        db.session.add(category)
        return db.session.commit()