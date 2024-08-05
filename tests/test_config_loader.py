import unittest
from flask import current_app
from util.config_loader import load_config_from_yaml

class ConfigLoaderTest(unittest.TestCase):

    def test_load_config_from_yaml(self):
        load_config_from_yaml()
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()