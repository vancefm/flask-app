import unittest
from flask import current_app
from app import app
from utils.config_loader import ConfigLoader

class ConfigLoaderTest(unittest.TestCase):

    def setUp(self):
        
        self.test_app = ConfigLoader().load_app()


    def test_yaml_import(self):
        
        print(f"Config path: {self.test_app.config['CUSTOM_CONFIG_PATH']}")
        self.assertTrue(self.test_app.config['CUSTOM_CONFIG_PATH'])

    def test_database_config(self):
        print(f"Database config: {self.test_app.config['DATABASE']}")
        self.assertTrue(self.test_app.config['DATABASE'])

if __name__ == "__main__":
    unittest.main()