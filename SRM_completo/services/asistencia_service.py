from datetime import date
from database.connection import get_connection

def registrar_asistencia(alumno_id, estado, fecha=None):
    fecha = fecha or date.today().isoformat()
    conn=get_connection()
    conn.execute("""INSERT INTO asistencias(alumno_id,fecha,estado)
                    VALUES(?,?,?)
                    ON CONFLICT(alumno_id,fecha) DO UPDATE SET estado=excluded.estado""",
                 (alumno_id,fecha,estado))
    conn.commit(); conn.close()

def listar_asistencia_hoy():
    conn=get_connection()
    rows=conn.execute("""SELECT a.*, al.nombre, al.apellido, al.curso
                         FROM asistencias a JOIN alumnos al ON al.id=a.alumno_id
                         WHERE a.fecha=date('now','localtime')
                         ORDER BY al.apellido,al.nombre""").fetchall()
    conn.close()
    return rows
