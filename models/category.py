
class Category:

    def __init__(self, name, match_patterns=None, subcategories=None):
        self.name = name
        self.match_patterns = match_patterns if match_patterns else []
        self.subcategories = [SubCategory(**sub) for sub in subcategories] if subcategories else []

    def __repr__(self):
        return f"Category({self.name}, {self.match_patterns}, {self.subcategories})"


class SubCategory(Category):
    def __init__(self, name, match_patterns=None):
        super().__init__(name, match_patterns)

    def __repr__(self):
        return f"SubCategory({self.name}, {self.match_patterns})"