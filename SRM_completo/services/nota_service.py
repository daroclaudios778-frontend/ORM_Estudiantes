from database.connection import get_connection

def registrar_nota(alumno_id,materia,periodo,nota):
    conn=get_connection()
    conn.execute("INSERT INTO notas(alumno_id,materia,periodo,nota) VALUES(?,?,?,?)",
                 (alumno_id,materia,periodo,nota))
    conn.commit(); conn.close()

def listar_notas():
    conn=get_connection()
    rows=conn.execute("""SELECT n.*, a.nombre, a.apellido
                         FROM notas n JOIN alumnos a ON a.id=n.alumno_id
                         ORDER BY a.apellido,a.nombre,n.materia,n.periodo""").fetchall()
    conn.close()
    return rows
