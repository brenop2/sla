from models.db import db
from models.user.roles import Role
from models.user import User

def create_db(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        # Creating roles
        Role.save_role("Admin", "Usuário full")
        Role.save_role("User", "Usuário com limitações")
        # Creating admin user
        User.save_user("Admin", "admin", "admin@admin.com", "admin")
