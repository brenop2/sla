# controllers/users_controller.py (ATUALIZAÇÃO)

from flask import Blueprint, request, render_template, redirect, url_for
from models.user.roles import Role
from models.user.users import User

user_ = Blueprint("user_", __name__, template_folder="views")

# ... (rotas register_user e add_user)

@user_.route('/register_user')
def register_user():
    """Rota para a tela de cadastro de usuário, passando a lista de roles."""
    roles = Role.get_role()
    return render_template("register_user.html", roles=roles)

@user_.route('/add_user', methods=['POST'])
def add_user():
    """Recebe os dados do formulário de cadastro e salva o novo usuário."""
    if request.method == 'POST':
        role_name = request.form['role_type_']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        User.save_user(role_name, username, email, password)
        
        return render_template("home.html")

# ====================================================================
# NOVAS ROTAS DE CRUD (Exercícios 9, 10, 11)
# ====================================================================

@user_.route('/users')
def users():
    """Lista todos os usuários. [Exercício 9]"""
    users = User.get_users()
    return render_template("users.html", users=users)

@user_.route('/edit_user')
def edit_user():
    """Carrega os dados de um usuário e todos os roles para edição. [Exercício 10]"""
    id = request.args.get('id', None)
    user = User.get_single_user(id)
    roles = Role.get_role() # Necessário para o dropdown de função
    return render_template("update_user.html", user=user[0] if user else None, roles=roles)

@user_.route('/update_user', methods=['POST'])
def update_user():
    """Recebe os dados editados (POST) e atualiza o usuário. [Exercício 10]"""
    if request.method == 'POST':
        id = request.form['id']
        username = request.form['username']
        email = request.form['email']
        password = request.form.get('password') # Senha pode ser nula se não for alterada
        role_name = request.form['role_type_']
        
        User.update_user(id, username, email, password, role_name)
        
        return redirect(url_for('user_.users'))

@user_.route('/del_user', methods=['GET'])
def del_user():
    """Deleta um usuário pelo ID. [Exercício 11]"""
    id = request.args.get('id', None)
    User.delete_user(id)
    return redirect(url_for('user_.users'))     