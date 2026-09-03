import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE = DATA_DIR / "srm.db"
DATA_DIR.mkdir(exist_ok=True)

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS alumnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dni TEXT NOT NULL UNIQUE,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        fecha_nacimiento TEXT,
        curso TEXT,
        telefono TEXT,
        email TEXT,
        observaciones TEXT,
        activo INTEGER DEFAULT 1
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cursos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        division TEXT NOT NULL,
        turno TEXT NOT NULL,
        anio INTEGER NOT NULL,
        activo INTEGER DEFAULT 1,
        UNIQUE(nombre, division, turno, anio)
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        rol TEXT NOT NULL DEFAULT 'DOCENTE',
        activo INTEGER DEFAULT 1
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS asistencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alumno_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        estado TEXT NOT NULL,
        UNIQUE(alumno_id, fecha),
        FOREIGN KEY(alumno_id) REFERENCES alumnos(id)
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS notas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alumno_id INTEGER NOT NULL,
        materia TEXT NOT NULL,
        periodo TEXT NOT NULL,
        nota REAL NOT NULL,
        FOREIGN KEY(alumno_id) REFERENCES alumnos(id)
    )""")
    if cur.execute("SELECT id FROM usuarios WHERE username='admin'").fetchone() is None:
        cur.execute("""INSERT INTO usuarios(username,password,nombre,apellido,rol)
                       VALUES('admin','admin123','Administrador','Sistema','ADMIN')""")
    conn.commit()
    conn.close()
