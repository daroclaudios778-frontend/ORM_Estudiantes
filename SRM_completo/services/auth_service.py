from database.connection import get_connection
from nicegui import app

def iniciar_sesion(username, password):
    conn = get_connection()
    user = conn.execute("""SELECT * FROM usuarios
                           WHERE username=? AND password=? AND activo=1""",
                        (username, password)).fetchone()
    conn.close()
    return user

def usuario_logueado():
    return "usuario_id" in app.storage.user

def cerrar_sesion():
    app.storage.user.clear()
