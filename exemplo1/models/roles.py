# models/user/roles.py

from models.db import db

class Role(db.Model):
    __tablename__ = 'roles'
    
    # Colunas da tabela 'roles'
    [cite_start]id = db.Column("id", db.Integer(), primary_key=True) [cite: 1058]
    [cite_start]name = db.Column(db.String(50), nullable=False, unique=True) [cite: 1059]
    [cite_start]description = db.Column(db.String(512)) [cite: 1060]
    
    @classmethod
    def save_role(cls, name, description):
        [cite_start]"""Cria e salva um novo Role no banco de dados. [cite: 1066, 1067, 1068, 1069]"""
        [cite_start]role = cls(name=name, description=description) [cite: 1067]
        [cite_start]db.session.add(role) [cite: 1068]
        [cite_start]db.session.commit() [cite: 1069]
        
    @classmethod
    def get_single_role(cls, name):
        [cite_start]"""Recupera um único Role pelo nome. [cite: 1081]"""
        role = cls.query.filter(cls.name == name).first()
        return role
        
    @classmethod
    def get_role(cls):
        [cite_start]"""Recupera todos os Roles. [cite: 1083]"""
        role = cls.query.all()
        return role