# utils/create_db.py
# Diretório: EXEMPLO2/utils/

from flask import Flask
# Importa todos os models (incluindo Role e User) e db do models/__init__.py
from models import *
from models.db import db 

def create_db(app: Flask):
    """
    Cria a estrutura do banco de dados e insere os dados iniciais (Roles e Admin).
    """
    with app.app_context():
        # Limpa e recria todas as tabelas
        db.drop_all()
        db.create_all()
        
        # 1. Criação dos Roles
        Role.save_role("Admin", "Usuário full")
        Role.save_role("User", "Usuário com limitações")
        
        # 2. Criação do Usuário Admin padrão
        User.save_user("Admin", "Admin", "admin", "admin")