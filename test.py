from config import TestingConfig, Config
from app import create_app

class Testing():

    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.ctx = app.app_context()
        self.ctx.push()


    def test_CourseRegistration(self):
        ...


Testing(create_app(Config), db)