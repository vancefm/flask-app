import unittest
from utils.config_loader import ConfigLoader
from data.models import db, Transaction, Category, CategoryPattern
from sqlalchemy import func, select

class DatabaseTest(unittest.TestCase):

    def setUp(self):
        self.app = ConfigLoader().load_app()

    def test_transaction_model(self):
        
        with self.app.app_context():
            count = db.session.scalar(select(func.count(Transaction.id)))
            self.assertGreater(count, 0)

            tx = db.session.query(Transaction).get(1)
            print(tx)
            self.assertTrue(tx)