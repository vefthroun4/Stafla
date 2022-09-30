import re
import os

class Database:
    def __init__(self):
        ...

    def setup_initial_state(self, app, db):
        # Enforces FK constraints
        from sqlalchemy import event
        with app.app_context():    
            @event.listens_for(db.engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

    def create_database(self, app, db):
        # Checks wheter .db file exists, if not it will create it.
        dbname = re.search("\\\\[A-Z|a-z]+\.db", app.config["SQLALCHEMY_DATABASE_URI"])
        if dbname and not os.path.exists(app.instance_path+dbname.group()):
            with app.app_context():
                from app.models import UserStatus
                db.create_all()
                
                # Temporary fix to allow login
                db.session.add(UserStatus(status_name="User"))
                db.session.commit()


    def init_app(self, app, db):
        self.setup_initial_state(app, db)
        self.create_database(app, db)