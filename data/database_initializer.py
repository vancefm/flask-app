from flask import current_app
from data.models import Category, CategoryPattern
from services import categories_service, category_patterns_service
import yaml
import traceback

def initialize_database():
    # Initializes the database according to database init files
    with current_app.app_context():
        try:
                process_categories()
                                
        except Exception as e:
            current_app.logger.critical(f"{e}\n{traceback.format_exc()}")

def process_categories() -> None:

    current_app.logger.info("Processing Categories...")
    
    with current_app.app_context():
        try:
            categories_path = current_app.config['DATA']['CATEGORIES_LIST_PATH']
            with open(categories_path, 'r') as cat_file:
                cat_data = yaml.safe_load(cat_file)
                cat_list = cat_data['Categories']
                current_app.logger.debug(f"Loaded categories file: {categories_path}")
                for category in cat_list:

                    if category['name'] != None:

                        # Check to see if we're dealing with a parent or child category

                        category_id = int()

                        if category['parent_name'] == None:
                            
                            # Parent categories do not have parent names.
                            # This is a parent category
                            # Check if parent category exists already
                            parent_id = categories_service.get_parent_id(category['name'])
                            if parent_id == None:
                                
                                # This parent category doesn't exist yet, we should create it
                                parent_id = categories_service.save_category(Category(category['name'], None))
                                category_id = parent_id
                                current_app.logger.debug(f"Created parent category {category['name']}:{parent_id}")
                            else:
                                category_id = parent_id
                                current_app.logger.debug(f"Parent category {category['name']} with parent id {parent_id} already exists. Skipping.")

                        else:

                            # Children categories do have parent name.
                            # This is a child category
                            # Check if the parent category exists
                            parent_id = categories_service.get_parent_id(category['parent_name'])
                            if parent_id == None:
                                parent_id = categories_service.save_category(Category(category['parent_name'], None))
                            
                            # The parent should exist now. Then handle the child category
                            # Check if the child exists already
                            child_id = categories_service.get_id_by_name_and_parent_id(category['name'], parent_id)
                            if child_id == None:
                                # This child doesn't exist, we should create it
                                category_id = categories_service.save_category(Category(category['name'], parent_id))
                                current_app.logger.debug(f"Created child category {category['name']}:{parent_id}")
                            else:
                                category_id = child_id
                                current_app.logger.debug(f"Child category {category['name']} with parent id {parent_id} already exists. Skipping.")

                        # Categories may have patterns we should match against,
                        # we should handle those now since we have a category id
                        for pattern in category['match_pattern'] or []:
                            process_patterns(pattern, category_id, category['name'])

                    else:
                        current_app.logger.error("Category missing name value")

        except Exception as e:
            current_app.logger.critical(f"{e}\n{traceback.format_exc()}")

def process_patterns(pattern: str, category_id: int, category_name: str):
    if pattern:
        if category_patterns_service.get_category_pattern_from_pattern(pattern) == None:
            category_patterns_service.save_category_pattern(CategoryPattern(category_id=category_id, pattern=pattern))
            current_app.logger.debug(f"Pattern \"{pattern}\" added for category {category_name}")
        else:
            current_app.logger.debug(f"Skipping pattern \"{pattern}\" for {category_name}, pattern already exists for a category")
    else:
        current_app.logger.debug(f"Skipping pattern \"{pattern}\" for {category_name}, none defined")