# models/user/users.py (ATUALIZAÇÃO)

from models.db import db
from models.user.roles import Role
from werkzeug.security import generate_password_hash, check_password_hash # Adicionar check_password_hash

class User(db.Model):
    __tablename__ = "users"
    
    # ... (atributos da classe: id, role_id, username, email, password)

    # ... (método save_user)

    @classmethod
    def get_users(cls):
        """Recupera todos os usuários com o nome do Role associado. [Exercício 9]"""
        # Faz um JOIN com a tabela Role e seleciona as colunas necessárias
        users = cls.query.join(Role, Role.id == cls.role_id)\
            .add_columns(cls.id, cls.username, cls.email, Role.name.label('role_name'))\
            .all()
        return users

    @classmethod
    def get_single_user(cls, id):
        """Busca um único usuário e seu Role pelo ID para edição."""
        user = cls.query.filter(cls.id == id)\
            .join(Role)\
            .add_columns(cls.id, cls.username, cls.email, Role.name.label('role_name'))\
            .first()
        return [user] if user is not None else []

    @classmethod
    def update_user(cls, id, username, email, password, role_name):
        """Atualiza o nome, email, senha (obrigatório) e função do usuário. [Exercício 10]"""
        user = cls.query.filter(cls.id == id).first()
        role = Role.get_single_role(role_name)
        
        if user is not None and role is not None:
            user.username = username
            user.email = email
            user.role_id = role.id
            
            # A senha é obrigatória na atualização (conforme Exercício 10)
            if password:
                user.password = generate_password_hash(password)
                
            db.session.commit()
            
        return cls.get_users()

    @classmethod
    def delete_user(cls, id):
        """Exclui um usuário. Impede a exclusão se o usuário for 'Admin'. [Exercício 11]"""
        user = cls.query.filter(cls.id == id).first()
        
        if user is not None:
            # Verifica se o Role é 'Admin'
            role = Role.query.filter(Role.id == user.role_id).first()
            
            if role and role.name != 'Admin':
                db.session.delete(user)
                db.session.commit()
        
        return cls.get_users()