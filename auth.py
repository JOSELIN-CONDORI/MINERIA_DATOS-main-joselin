from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

# Crear un blueprint para la autenticación
auth = Blueprint('auth', __name__)

# Modelo de usuario
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# Función para crear la conexión a la base de datos
def crear_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='web_scraping_db'
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Ruta de registro
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conexion = crear_conexion()
        cursor = conexion.cursor()

        # Verificar si el usuario ya existe
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            flash("El usuario ya existe")
            return redirect(url_for('auth.register'))

        # Registrar al usuario
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conexion.commit()
        cursor.close()
        conexion.close()

        flash("Registro exitoso. Ahora puedes iniciar sesión.")
        return redirect(url_for('auth.login'))

    return render_template('register.html')

# Ruta de login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conexion = crear_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        cursor.close()
        conexion.close()

        if user and check_password_hash(user['password'], password):
            user_obj = User(id=user['id'], username=user['username'])
            login_user(user_obj)
            flash("Inicio de sesión exitoso")
            return redirect(url_for('scraping_page'))
        else:
            flash("Nombre de usuario o contraseña incorrectos")
            return redirect(url_for('auth.login'))

    return render_template('login.html')

# Ruta de logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión")
    return redirect(url_for('auth.login'))
