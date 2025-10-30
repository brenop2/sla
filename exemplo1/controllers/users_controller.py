from flask import Blueprint, request, render_template, redirect, url_for
from models.user import User, Role

user_ = Blueprint("user_", __name__, template_folder="views")

@user_.route('/register_user')
def register_user():
    roles = Role.query.all()
    return render_template("register_user.html", roles=roles)

@user_.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    role_type_ = request.form['role']
    
    User.save_user(role_type_, username, email, password)
    return redirect(url_for('user_.register_user'))
