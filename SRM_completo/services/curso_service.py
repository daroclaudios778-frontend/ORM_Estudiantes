from database.connection import get_connection


def listar_cursos():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM cursos WHERE activo=1 ORDER BY anio, nombre, division"
    ).fetchall()
    conn.close()
    return rows


def crear_curso(nombre, division, turno, anio):
    conn = get_connection()
    conn.execute(
        "INSERT INTO cursos(nombre, division, turno, anio) VALUES(?,?,?,?)",
        (nombre.strip(), division.strip(), turno, anio),
    )
    conn.commit()
    conn.close()


def actualizar_curso(id, nombre, division, turno, anio):
    conn = get_connection()
    conn.execute(
        """UPDATE cursos SET nombre=?, division=?, turno=?, anio=?
           WHERE id=?""",
        (nombre.strip(), division.strip(), turno, anio, id),
    )
    conn.commit()
    conn.close()


def eliminar_curso(id):
    conn = get_connection()
    conn.execute("UPDATE cursos SET activo=0 WHERE id=?", (id,))
    conn.commit()
    conn.close()
