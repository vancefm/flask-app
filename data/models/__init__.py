from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from data.models.category import Category
from data.models.transaction import Transaction
from data.models.category_pattern import CategoryPattern
