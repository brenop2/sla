from models.db import db
from models.user.roles import Role

class User(db.Model):
    __tablename__ = "users"

    id = db.Column("id", db.Integer(), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id))
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    def save_user(role_type_, username, email, password):
        role = Role.query.filter_by(name=role_type_).first()
        user = User(role_id=role.id, username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
