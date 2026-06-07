from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'restaurante$2024#colombia*admin'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///delicias.db'

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/menu')
def menu():
    if not session.get('usuario_logueado'):
        return redirect(url_for('login'))
    return render_template('menu.html')

@app.route('/desayunos')
def desayunos():
    return render_template('desayunos.html')

@app.route('/almuerzos')
def almuerzos():
    comidas = [
        {"titulo":"Sancocho de Sábalo", "descripcion":"Caldo contundente de pescado...", "imagen":"img/huevos-fritos.jpg", "estrellas":4},
        {"titulo":"Mote de Queso", "descripcion":"Sopa espesa de ñame...", "imagen":"img/arepas.jpg", "estrellas":5},
        {"titulo":"Viuda de Pescado", "descripcion":"Pescado de río cocinado...", "imagen":"img/carimanolas.jpeg", "estrellas":4}
    ]
    return render_template('almuerzos.html', comidas=comidas)

@app.route('/registro', methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_nacimiento = request.form['fecha_nacimiento']
        email = request.form['email']
        pasword = request.form['pasword']

        if not nombre or not apellido or not fecha_nacimiento or not email or not pasword:
            return 'todos los campos deben estar llenos'

        db.session.execute(
            db.text('INSERT INTO usuarios (nombre, apellido, fecha_nacimiento, email, password) VALUES (:nombre, :apellido, :fecha_nacimiento, :email, :pasword)'),
            {'nombre': nombre, 'apellido': apellido, 'fecha_nacimiento': fecha_nacimiento, 'email': email, 'pasword': pasword}
        )
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('registro.html')

@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        admin = request.form['admin']
        pasword = request.form['pasword']
        credenciales = ('admin04@gmail.com', '1234')

        if not admin or not pasword:
            return 'los campos deben estar llenos'
        elif admin == credenciales[0] and pasword == credenciales[1]:
            session['admin_logueado'] = True
            return redirect(url_for('panel_creacion_productos'))
        else:
            return render_template('error.html')

    return render_template('admin.html')

@app.route('/panel_creacion_productos')
def panel_creacion_productos():
    if not session.get('admin_logueado'):
        return redirect(url_for('admin'))
    return render_template('panel_creacion_productos.html')

@app.route('/panel_creacion_bebidias')
def panel_creacion_bebidas():
    return render_template('panel_creacion_bebidas.html')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pasword = request.form['pasword']

        if not email or not pasword:
            return 'ningun campo debe estar vacio'

        resultado = db.session.execute(
            db.text('SELECT * FROM usuarios WHERE email = :email AND password = :pasword'),
            {'email': email, 'pasword': pasword}
        ).fetchone()

        if resultado:
            session['usuario_logueado'] = True
            return redirect(url_for('menu'))
        else:
            return 'correo o contraseña incorrectos'

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)