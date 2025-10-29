# models/user/roles.py
# Diretório: EXEMPLO2/models/user/

from models.db import db

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column("id", db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(512))
    
    @classmethod
    def save_role(cls, name, description):
        """Cria e salva um novo Role."""
        role = cls(name=name, description=description)
        db.session.add(role)
        db.session.commit()
        
    @classmethod
    def get_single_role(cls, name):
        """Recupera um único Role pelo nome."""
        return cls.query.filter(cls.name == name).first()
        
    @classmethod
    def get_role(cls):
        """Recupera todos os Roles."""
        return cls.query.all()