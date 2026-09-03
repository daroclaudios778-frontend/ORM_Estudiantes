from database.connection import get_connection

def listar_alumnos():
    conn=get_connection()
    rows=conn.execute("SELECT * FROM alumnos WHERE activo=1 ORDER BY apellido,nombre").fetchall()
    conn.close()
    return rows

def crear_alumno(dni,nombre,apellido,fecha_nacimiento=None,curso=None,telefono=None,email=None,observaciones=None):
    conn=get_connection()
    conn.execute("""INSERT INTO alumnos(dni,nombre,apellido,fecha_nacimiento,curso,telefono,email,observaciones)
                    VALUES(?,?,?,?,?,?,?,?)""",
                 (dni,nombre,apellido,fecha_nacimiento,curso,telefono,email,observaciones))
    conn.commit(); conn.close()

def actualizar_alumno(id,dni,nombre,apellido,fecha_nacimiento,curso,telefono,email,observaciones):
    conn=get_connection()
    conn.execute("""UPDATE alumnos SET dni=?,nombre=?,apellido=?,fecha_nacimiento=?,curso=?,telefono=?,email=?,observaciones=?
                    WHERE id=?""",
                 (dni,nombre,apellido,fecha_nacimiento,curso,telefono,email,observaciones,id))
    conn.commit(); conn.close()

def eliminar_alumno(id):
    conn=get_connection()
    conn.execute("UPDATE alumnos SET activo=0 WHERE id=?", (id,))
    conn.commit(); conn.close()
