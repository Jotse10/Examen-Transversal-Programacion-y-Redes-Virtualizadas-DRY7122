from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'usuarios.db'

def init_db():
    """Crea la base de datos y la tabla de usuarios si no existen."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inicializa la base de datos
init_db()

@app.route('/')
def home():
    """Muestra la primera fase del contenido web."""
    return "<h1>Bienvenido a la Gestión de Credenciales</h1>"

@app.route('/registro', methods=['POST'])
def registro():
    """
    Registra un usuario nuevo.
    Se esperan los parámetros 'username' y 'password' vía solicitud POST.
    """
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return jsonify({"mensaje": "Faltan datos"}), 400
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    
    return jsonify({"mensaje": f"Usuario {username} registrado exitosamente"}), 201

@app.route('/login', methods=['POST'])
def login():
    """
    Verifica las credenciales del usuario.
    Se reciben 'username' y 'password' vía POST y se consulta en la BD.
    """
    username = request.form.get('username')
    password = request.form.get('password')
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (username, password))
    usuario = cursor.fetchone()
    conn.close()
    
    if usuario:
        return jsonify({"mensaje": "Acceso concedido"}), 200
    else:
        return jsonify({"mensaje": "Credenciales incorrectas"}), 401

if __name__ == '__main__':
    # Ejecuta la aplicación en el puerto 5800
    app.run(port=5800, debug=True)
