import unittest
from flask import current_app
from app import db, create_app
from app.models import User

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()

    def test_app_exits(self):
        user = User(username='jinshao',password='shiluodalu')
        db.session.add(user)
        db.session.commit()