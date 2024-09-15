from flask import current_app
from data.models import Category, CategoryPattern
from services import categories_service, category_patterns_service
import yaml
import traceback

def initialize_database():
    # Initializes the database according to database init files
    with current_app.app_context():
        try:
                categories_path = current_app.config['DATA']['CATEGORIES_LIST_PATH']
                with open(categories_path, 'r') as cat_file:
                    cat_data = yaml.safe_load(cat_file)
                    current_app.logger.debug(f"Loaded categories file: {categories_path}")

                    # START CATEGORIES
                    # Load the categories loaded from the yaml file into the database
                    for yaml_category in cat_data["Categories"]:

                        cat_name = yaml_category['name']
                        cat_parent_name = yaml_category['parent_category_name']
                        cat_parent_id = categories_service.get_parent_id_from_parent_name(cat_parent_name)
                        
                        current_app.logger.debug(f"Processing category: {cat_parent_name or '<>'} : {cat_name}")

                        # Check if this is intended to be a parent category
                        if cat_parent_name is None:

                            process_parent_category(cat_name)
                            
                        else:
                            # This is intended to be a child category
                            process_child_category(cat_parent_name, cat_name)
 
                        # END CATEGORIES 

                        # START CATEGORY PATTERNS
                        
                        # Make sure the pattern for this category exist
                        pattern_list = yaml_category['match_pattern']
                        for pattern in pattern_list or []:
                            process_patterns(pattern, cat_name, cat_parent_id)
                            
                        # END CATEGORY PATTERNS
                                
        except Exception as e:
            current_app.logger.critical(f"{e}\n{traceback.format_exc()}")

def process_parent_category(cat_name):
    # Add the category if it doesn't exist as a parent
    if categories_service.get_parent_by_name(cat_name) is None:
        current_app.logger.debug(f"Parent category {cat_name} does not exist yet")
        categories_service.save_category(Category(category_name=cat_name, parent_id=None))
        current_app.logger.debug(f"Successfully added parent category {cat_name}")
        cat_parent_id = categories_service.get_parent_id_from_parent_name(cat_name)
    else:
        current_app.logger.debug(f"Skipping parent category, {cat_name} already exists")

def process_child_category(cat_parent_name, cat_name):
    cat_parent_id = categories_service.get_parent_id_from_parent_name(cat_parent_name)
    # Make sure the parent exists first.
    if categories_service.get_parent_by_name(cat_parent_name) is None:
        current_app.logger.debug(f"Parent category {cat_parent_name} does not exist yet")
        categories_service.save_category(Category(cat_parent_name))
        current_app.logger.debug(f"Successfully added parent category {cat_parent_name} for {cat_name}")
        cat_parent_id = categories_service.get_parent_id_from_parent_name(cat_parent_name)

    ## Add the category if it doesn't exist as a child
    if categories_service.get_id_by_name_and_parent_id(cat_name, cat_parent_id) is None:
        current_app.logger.debug(f"Child category {cat_name} does not exist yet for parent: {cat_parent_id}")
        categories_service.save_category(Category(category_name=cat_name, parent_id=cat_parent_id))
        current_app.logger.debug(f"Successfully added child category {cat_name} for {cat_parent_name}")
    else:
        current_app.logger.debug(f"Skippping child category, {cat_parent_name}: {cat_name} already exists")



def process_patterns(pattern, cat_name, cat_parent_id ):
    if pattern:
        if category_patterns_service.get_category_pattern_from_pattern(pattern) is None:
            cat_id = categories_service.get_id_by_name_and_parent_id(name=cat_name, parent_id=cat_parent_id)
            category_patterns_service.save_category_pattern(CategoryPattern(category_id=cat_id, pattern=pattern))
        else:
            current_app.logger.debug(f"Skipping pattern \"{pattern}\" for {cat_name}, pattern already exists")
    else:
        current_app.logger.debug(f"Skipping pattern \"{pattern}\" for {cat_name}, none defined")