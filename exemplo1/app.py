from flask import Flask, render_template, request, redirect, url_for, flash, abort
import os
from datetime import datetime, timedelta

# --- IMPORTAÇÃO DE BLUEPRINTS E DADOS ---
# ATENÇÃO: É ESSENCIAL que os arquivos 'sensors.py' e 'actuators.py' existam
from sensors import sensors as sensors_api, sensor_data
from actuators import actuators as actuators_api, actuator_status

# --- FLASK-LOGIN ---
from flask_login import (
    LoginManager, UserMixin, login_user,
    login_required, logout_user, current_user
)

app = Flask(__name__)
# Chave secreta obrigatória para Flash e Sessões
app.secret_key = "segredo_super_seguro"

# --- CONFIGURAÇÃO FLASK-LOGIN ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Handler Customizado para Acesso Não Autorizado (Erro 401)
@login_manager.unauthorized_handler
def unauthorized():
    """Chamado quando @login_required falha (usuário não logado)"""
    flash('Você precisa fazer login para acessar esta página!', 'warning')
    # O handler 401 do @app.errorhandler(401) será chamado automaticamente
    return render_template('401.html'), 401

# Usuários em memória (Simulação de Banco de Dados)
users = {"admin": "1234", "joao": "4567"}

# Classe User para Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

# --- CONFIGURAÇÃO DE UPLOAD ---
UPLOAD_FOLDER = 'static/img'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- ROTAS DE LOGIN/LOGOUT ---

@app.route('/')
def index():
    return redirect(url_for("login"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = request.form['user']
        password = request.form['password']
        if user in users and users[user] == password:
            login_user(User(user))
            flash(f'Bem-vindo, {user}!', 'success')
            return redirect(url_for('home'))
        
        flash('Credenciais inválidas!', 'danger')
        return redirect(url_for('login'))
        
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Você saiu com sucesso!', 'info')
    return redirect(url_for("login"))

# --- PÁGINAS PROTEGIDAS ---

@app.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user.id)

@app.route('/admin')
@login_required
def admin_area():
    """Área restrita: Verifica se o usuário é 'admin'."""
    if current_user.id != 'admin':
        # Dispara o erro 403 com uma mensagem de contexto
        flash("Seu usuário não tem permissão de administrador para acessar esta área.", 'danger')
        abort(403) 
    return render_template('admin.html', title='Área de Administração')

# --- ROTAS PARA TESTAR ERROR HANDLERS (Simulação de Erros) ---

@app.route('/test/404')
def test_404():
    abort(404)

@app.route('/test/403')
@login_required
def test_403():
    abort(403)

@app.route('/test/500')
def test_500():
    # Força uma exceção para testar o handler 500
    raise Exception("Erro intencional no servidor para teste")

@app.route('/test/408')
@login_required
def test_408():
    """Força um erro 408 (Request Timeout)"""
    abort(408)

# Simulação de limite de taxa (Rate Limit)
request_counts = {}

@app.route('/test/429')
@login_required
def test_429():
    """Simula Too Many Requests (Limite de Taxa)"""
    user_id = current_user.id if current_user.is_authenticated else 'guest'
    now = datetime.now()
    
    # Remove contagens antigas (limite de 1 minuto)
    request_counts[user_id] = [t for t in request_counts.get(user_id, []) if now - t < timedelta(seconds=60)]
    request_counts[user_id].append(now)
    
    # Limite de 5 requisições por minuto
    if len(request_counts[user_id]) > 5:
        # Retorna o template 429 e o cabeçalho 'Retry-After'
        return render_template('429.html'), 429, {'Retry-After': '60'}
    
    flash(f"Teste 429: Requisição permitida ({len(request_counts[user_id])} de 5)", 'info')
    return redirect(url_for('home'))

@app.route('/test/503')
def test_503():
    """Força Serviço Indisponível (503)"""
    abort(503)

# --- UPLOAD DE ARQUIVOS ---
@app.route('/upload_file', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash("Nenhum arquivo enviado", "warning")
        return redirect(url_for('home'))
    f = request.files['file']
    if f.filename == '':
        flash("Arquivo inválido", "warning")
        return redirect(url_for('home'))
        
    f.save(os.path.join(UPLOAD_FOLDER, f.filename))
    flash(f"Arquivo {f.filename} salvo com sucesso!", "success")
    return redirect(url_for('home'))

# --- USUÁRIOS (CRUD simples) ---

@app.route('/register_user')
@login_required
def register_user():
    return render_template('register_user.html')

@app.route('/add_user', methods=['POST'])
@login_required
def add_user():
    global users
    user_name = request.form['user']
    password = request.form['password']
    
    if user_name in users:
        flash(f'Usuário {user_name} já existe!', 'warning')
        return redirect(url_for('register_user'))
    
    users[user_name] = password
    flash(f'Usuário {user_name} cadastrado com sucesso!', 'success')
    return redirect(url_for('list_users'))

@app.route('/list_users')
@login_required
def list_users():
    return render_template('list_users.html', title='Lista de Usuários', devices=users)

@app.route('/remove_user')
@login_required
def remove_user():
    return render_template("remove_user.html", devices=users)

@app.route('/del_user', methods=['POST'])
@login_required
def del_user():
    global users
    user_to_delete = request.form['user']
    
    if user_to_delete == current_user.id:
        flash('Você não pode deletar seu próprio usuário!', 'danger')
        return redirect(url_for('list_users'))
    
    if user_to_delete in users:
        users.pop(user_to_delete)
        flash(f'Usuário {user_to_delete} removido com sucesso!', 'success')
    else:
        flash(f'Usuário {user_to_delete} não encontrado!', 'warning')
    
    return redirect(url_for('list_users'))

# --- SENSORES (CRUD) ---
@app.route('/register_sensor')
@login_required
def register_sensor():
    return render_template('register_sensor.html')

@app.route('/add_sensor', methods=['POST'])
@login_required
def add_sensor():
    global sensor_data
    sensor_id = request.form['id']
    location = request.form['location']
    unit = request.form['unit']
    
    if sensor_id in sensor_data:
        flash(f'Sensor {sensor_id} já existe!', 'warning')
        return redirect(url_for('register_sensor'))
    
    sensor_data[sensor_id] = {'value': 0, 'unit': unit, 'location': location}
    flash(f'Sensor {sensor_id} cadastrado com sucesso!', 'success')
    return redirect(url_for('list_sensors'))

@app.route('/sensors')
@login_required
def list_sensors():
    return render_template('sensors.html', title='Sensores', devices=sensor_data)

@app.route('/remove_sensor')
@login_required
def remove_sensor():
    return render_template('remove_sensor.html', devices=sensor_data)

@app.route('/del_sensor', methods=['POST'])
@login_required
def del_sensor():
    global sensor_data
    sensor_to_delete = request.form['sensor']
    if sensor_to_delete in sensor_data:
        sensor_data.pop(sensor_to_delete)
        flash(f'Sensor {sensor_to_delete} removido com sucesso!', 'success')
    else:
        flash(f'Sensor {sensor_to_delete} não encontrado!', 'warning')
    return redirect(url_for('list_sensors'))

# --- ATUADORES (CRUD) ---
@app.route('/register_actuator')
@login_required
def register_actuator():
    return render_template('register_actuator.html')

@app.route('/add_actuator', methods=['POST'])
@login_required
def add_actuator():
    global actuator_status
    actuator_id = request.form['id']
    location = request.form['location']
    
    if actuator_id in actuator_status:
        flash(f'Atuador {actuator_id} já existe!', 'warning')
        return redirect(url_for('register_actuator'))
    
    actuator_status[actuator_id] = {'state': 'off', 'location': location}
    flash(f'Atuador {actuator_id} cadastrado com sucesso!', 'success')
    return redirect(url_for('list_actuadores'))

@app.route('/actuators')
@login_required
def list_actuadores():
    return render_template('actuators.html', title='Atuadores', devices=actuator_status)

@app.route('/remove_actuator')
@login_required
def remove_actuator():
    return render_template('remove_actuator.html', devices=actuator_status)

@app.route('/del_actuator', methods=['POST'])
@login_required
def del_actuator():
    global actuator_status
    actuator_to_delete = request.form['actuator']
    if actuator_to_delete in actuator_status:
        actuator_status.pop(actuator_to_delete)
        flash(f'Atuador {actuator_to_delete} removido com sucesso!', 'success')
    else:
        flash(f'Atuador {actuator_to_delete} não encontrado!', 'warning')
    return redirect(url_for('list_actuadores'))


# --- ROTAS DE CÔMODOS ---
@app.route('/bedroom')
@login_required
def bedroom():
    menu_items = {'Sensores': url_for('bedroom_sensors'), 'Atuadores': url_for('bedroom_actuators')}
    return render_template('bedroom.html', title='Quarto', menu_items=menu_items)

@app.route('/bedroom/sensors')
@login_required
def bedroom_sensors():
    sensors_data = {'Luminosidade': 500}
    return render_template('bedroom_sensors.html', title='Sensores do Quarto', 
                           devices=sensors_data, back_url=url_for('bedroom'), room_name='Quarto')

@app.route('/bedroom/actuators')
@login_required
def bedroom_actuators():
    actuators_data = {'Interruptor': 1}
    return render_template('bedroom_actuators.html', title='Atuadores do Quarto', 
                           devices=actuators_data, back_url=url_for('bedroom'), room_name='Quarto')

@app.route('/bathroom')
@login_required
def bathroom():
    menu_items = {'Sensores': url_for('bathroom_sensors'), 'Atuadores': url_for('bathroom_actuators')}
    return render_template('bathroom.html', title='Banheiro', menu_items=menu_items)

@app.route('/bathroom/sensors')
@login_required
def bathroom_sensors():
    sensors_data = {'Umidade': 80}
    return render_template('bathroom_sensors.html', title='Sensores do Banheiro', 
                           devices=sensors_data, back_url=url_for('bathroom'), room_name='Banheiro')

@app.route('/bathroom/actuators')
@login_required
def bathroom_actuators():
    actuators_data = {'Lâmpada Inteligente': 0}
    return render_template('bathroom_actuators.html', title='Atuadores do Banheiro', 
                           devices=actuators_data, back_url=url_for('bathroom'), room_name='Banheiro')

# --- TRATAMENTO DE ERROS GLOBAIS ---
# Estes handlers serão chamados para erros que não foram tratados localmente no Blueprint

@app.errorhandler(400)
def bad_request(error):
    return render_template('400.html', error_code=400), 400

@app.errorhandler(401)
def unauthorized_error(error):
    return render_template('401.html', error_code=401), 401

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html', error_code=403), 403

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error_code=404), 404

@app.errorhandler(408)
def request_timeout(error):
    return render_template('408.html', error_code=408), 408

@app.errorhandler(429)
def too_many_requests_global(error):
    return render_template('429.html', error_code=429), 429

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error_code=500, error=error), 500

@app.errorhandler(503)
def service_unavailable(error):
    return render_template('503.html', error_code=503), 503

# --- REGISTRO DOS BLUEPRINTS ---
# Assumindo que sensors_api e actuators_api são os objetos Blueprint
app.register_blueprint(sensors_api, url_prefix='/api/sensores')
app.register_blueprint(actuators_api, url_prefix='/api/atuadores')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
