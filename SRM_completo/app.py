from nicegui import app, ui
from database.connection import initialize_database
from services.auth_service import usuario_logueado, cerrar_sesion, iniciar_sesion
from services.alumno_service import listar_alumnos, crear_alumno, actualizar_alumno, eliminar_alumno
from services.asistencia_service import registrar_asistencia, listar_asistencia_hoy
from services.nota_service import registrar_nota, listar_notas
from services.curso_service import listar_cursos, crear_curso, actualizar_curso, eliminar_curso

initialize_database()

def ir(ruta):
    ui.navigate.to(ruta)

def es_admin():
    return app.storage.user.get("rol") == "ADMIN"

def login_view():
    with ui.column().classes("w-full h-screen items-center justify-center bg-slate-100"):
        with ui.card().classes("w-[420px] p-8 shadow-xl"):
            ui.label("SRM").classes("text-4xl font-bold text-blue-700 text-center w-full")
            ui.label("Sistema de Registro Escolar").classes("text-center text-gray-500 w-full mb-6")
            usuario = ui.input("Usuario").classes("w-full")
            password = ui.input("Contraseña", password=True, password_toggle_button=True).classes("w-full")

            def entrar():
                user = iniciar_sesion(usuario.value, password.value)
                if not user:
                    ui.notify("Usuario o contraseña incorrectos", type="negative")
                    return
                app.storage.user.update({
                    "usuario_id": user["id"],
                    "username": user["username"],
                    "nombre": user["nombre"],
                    "apellido": user["apellido"],
                    "rol": user["rol"],
                })
                ir("/")

            ui.button("Ingresar", icon="login", on_click=entrar).classes("w-full mt-5")
            ui.separator().classes("my-4")
            ui.label("Usuario inicial: admin").classes("text-sm text-gray-500")
            ui.label("Contraseña inicial: admin123").classes("text-sm text-gray-500")

def guard():
    if not usuario_logueado():
        ir("/login")
        return False
    return True

def sidebar():
    with ui.left_drawer(value=True).classes("bg-slate-900 text-white p-4"):
        ui.label("🎓 SRM").classes("text-3xl font-bold")
        ui.label("Sistema de Registro Escolar").classes("text-xs text-slate-300 mb-6")

        ui.button("Dashboard", icon="dashboard", on_click=lambda: ir("/")).props("flat").classes("w-full justify-start")
        ui.label("GESTIÓN ACADÉMICA").classes("text-xs text-slate-400 mt-5 mb-2")
        ui.button("Alumnos", icon="school", on_click=lambda: ir("/alumnos")).props("flat").classes("w-full justify-start")
        ui.button("Asistencia", icon="event_available", on_click=lambda: ir("/asistencia")).props("flat").classes("w-full justify-start")
        ui.button("Notas", icon="grading", on_click=lambda: ir("/notas")).props("flat").classes("w-full justify-start")
        ui.button("Cursos", icon="groups", on_click=lambda: ir("/cursos")).props("flat").classes("w-full justify-start")
        ui.button("Docentes", icon="person", on_click=lambda: ui.notify("Módulo de docentes: siguiente etapa")).props("flat").classes("w-full justify-start")

        if es_admin():
            ui.label("ADMINISTRACIÓN").classes("text-xs text-slate-400 mt-5 mb-2")
            ui.button("Usuarios", icon="manage_accounts", on_click=lambda: ui.notify("Módulo de usuarios conectado al login")).props("flat").classes("w-full justify-start")
            ui.button("Reportes", icon="description", on_click=lambda: ui.notify("Reportes: siguiente etapa")).props("flat").classes("w-full justify-start")

        ui.space()
        ui.button("Cerrar sesión", icon="logout", on_click=lambda: (cerrar_sesion(), ir("/login"))).props("outline").classes("w-full")

def layout(titulo):
    sidebar()
    with ui.header().classes("bg-white text-slate-800 border-b items-center"):
        ui.label(titulo).classes("text-xl font-bold")
        ui.space()
        ui.label(f'{app.storage.user.get("nombre","")} {app.storage.user.get("apellido","")} · {app.storage.user.get("rol","")}').classes("text-sm")
    return ui.column().classes("w-full p-6")

def stat_card(titulo, valor, icono, extra=""):
    with ui.card().classes("flex-1 min-w-[190px]"):
        with ui.row().classes("items-center"):
            ui.icon(icono).classes("text-3xl text-blue-600")
            with ui.column().classes("gap-0"):
                ui.label(titulo).classes("text-gray-500")
                ui.label(str(valor)).classes("text-3xl font-bold")
                if extra:
                    ui.label(extra).classes("text-xs text-gray-500")

def dashboard():
    c = layout("Panel Principal")
    alumnos = listar_alumnos()
    asistencia = listar_asistencia_hoy()
    presentes = sum(1 for x in asistencia if x["estado"] == "PRESENTE")
    ausentes = sum(1 for x in asistencia if x["estado"] == "AUSENTE")
    notas = listar_notas()
    promedio = round(sum(x["nota"] for x in notas) / len(notas), 2) if notas else 0

    with c:
        with ui.row().classes("w-full gap-4 flex-wrap"):
            stat_card("Alumnos", len(alumnos), "groups", "Total registrados")
            stat_card("Asistencias hoy", presentes, "person", "Presentes")
            stat_card("Ausencias hoy", ausentes, "person_off", "Ausentes")
            stat_card("Promedio general", promedio, "school", "Notas cargadas")
            stat_card("Cursos activos", len(listar_cursos()), "class", "Cursos registrados")

        with ui.row().classes("w-full gap-4 items-stretch mt-4"):
            with ui.card().classes("flex-[2]"):
                ui.label("Alumnos recientes").classes("text-xl font-bold")
                rows = [{"DNI": a["dni"], "Alumno": f'{a["apellido"]}, {a["nombre"]}', "Curso": a["curso"] or "-"} for a in alumnos[-8:]]
                ui.table(columns=[
                    {"name":"DNI","label":"DNI","field":"DNI"},
                    {"name":"Alumno","label":"Alumno","field":"Alumno"},
                    {"name":"Curso","label":"Curso","field":"Curso"},
                ], rows=rows).classes("w-full")
            with ui.card().classes("flex-1"):
                ui.label("Asistencia de hoy").classes("text-xl font-bold")
                ui.label(f"Presentes: {presentes}").classes("text-green-600 text-lg")
                ui.label(f"Ausentes: {ausentes}").classes("text-red-600 text-lg")
                ui.button("Tomar asistencia", icon="event_available", on_click=lambda: ir("/asistencia")).classes("mt-4")

        with ui.row().classes("w-full gap-4 mt-4"):
            with ui.card().classes("flex-1"):
                ui.label("Acciones rápidas").classes("text-xl font-bold")
                ui.button("Agregar nuevo alumno", icon="person_add", on_click=lambda: ir("/alumnos")).classes("w-full")
                ui.button("Registrar asistencia", icon="fact_check", on_click=lambda: ir("/asistencia")).classes("w-full")
                ui.button("Cargar notas", icon="grading", on_click=lambda: ir("/notas")).classes("w-full")
            with ui.card().classes("flex-1"):
                ui.label("Resumen académico").classes("text-xl font-bold")
                ui.label(f"Notas registradas: {len(notas)}")
                ui.label(f"Promedio actual: {promedio}")
                ui.label("Sistema operativo y listo para ampliar.")

def formulario_alumno(refrescar, alumno=None):
    with ui.dialog() as dialog:
        with ui.card().classes("w-[620px]"):
            ui.label("Editar alumno" if alumno else "Agregar nuevo alumno").classes("text-2xl font-bold")
            dni = ui.input("DNI", value=alumno["dni"] if alumno else "").classes("w-full")
            nombre = ui.input("Nombre", value=alumno["nombre"] if alumno else "").classes("w-full")
            apellido = ui.input("Apellido", value=alumno["apellido"] if alumno else "").classes("w-full")
            with ui.row().classes("w-full"):
                fecha = ui.input("Fecha nacimiento", value=alumno["fecha_nacimiento"] if alumno else "").classes("flex-1")
                curso = ui.input("Curso", value=alumno["curso"] if alumno else "").classes("flex-1")
            with ui.row().classes("w-full"):
                telefono = ui.input("Teléfono", value=alumno["telefono"] if alumno else "").classes("flex-1")
                email = ui.input("Email", value=alumno["email"] if alumno else "").classes("flex-1")
            observaciones = ui.textarea("Observaciones", value=alumno["observaciones"] if alumno else "").classes("w-full")

            def guardar():
                if not dni.value or not nombre.value or not apellido.value:
                    ui.notify("DNI, nombre y apellido son obligatorios", type="warning")
                    return
                try:
                    if alumno:
                        actualizar_alumno(alumno["id"], dni.value, nombre.value, apellido.value, fecha.value, curso.value, telefono.value, email.value, observaciones.value)
                    else:
                        crear_alumno(dni.value, nombre.value, apellido.value, fecha.value, curso.value, telefono.value, email.value, observaciones.value)
                    dialog.close()
                    refrescar()
                    ui.notify("Alumno guardado correctamente", type="positive")
                except Exception as e:
                    ui.notify(f"Error: {e}", type="negative")

            with ui.row().classes("justify-end w-full"):
                ui.button("Cancelar", on_click=dialog.close).props("flat")
                ui.button("Guardar alumno", icon="save", on_click=guardar)
    dialog.open()

def alumnos_view():
    c = layout("Gestión de Alumnos")
    with c:
        with ui.row().classes("w-full items-center"):
            ui.label("Alumnos").classes("text-3xl font-bold")
            ui.space()
            ui.button("Nuevo alumno", icon="person_add", on_click=lambda: formulario_alumno(refrescar)).classes("bg-blue-600 text-white")

        buscador = ui.input("Buscar por DNI, nombre o apellido").classes("w-full mt-4")
        cont = ui.column().classes("w-full")

        def refrescar():
            cont.clear()
            texto = (buscador.value or "").lower()
            alumnos = [a for a in listar_alumnos() if texto in f'{a["dni"]} {a["nombre"]} {a["apellido"]}'.lower()]
            with cont:
                rows = [{"id":a["id"], "DNI":a["dni"], "Alumno":f'{a["apellido"]}, {a["nombre"]}', "Curso":a["curso"] or "-", "Teléfono":a["telefono"] or "-"} for a in alumnos]
                ui.table(columns=[
                    {"name":"DNI","label":"DNI","field":"DNI"},
                    {"name":"Alumno","label":"Alumno","field":"Alumno"},
                    {"name":"Curso","label":"Curso","field":"Curso"},
                    {"name":"Teléfono","label":"Teléfono","field":"Teléfono"},
                ], rows=rows).classes("w-full")
                for a in alumnos:
                    with ui.row().classes("w-full justify-end -mt-12 pr-4 pointer-events-none"):
                        pass
                with ui.row().classes("gap-2 mt-2"):
                    for a in alumnos:
                        ui.button(f'Editar {a["apellido"]}', icon="edit", on_click=lambda a=a: formulario_alumno(refrescar, a)).props("outline")
                        ui.button(f'Eliminar {a["apellido"]}', icon="delete", color="negative", on_click=lambda a=a: borrar(a, refrescar)).props("outline")

        def borrar(a, refresh):
            eliminar_alumno(a["id"])
            ui.notify("Alumno eliminado", type="positive")
            refresh()

        buscador.on_value_change(lambda e: refrescar())
        refrescar()

def asistencia_view():
    c = layout("Control de Asistencia")
    with c:
        ui.label("Asistencia de alumnos").classes("text-3xl font-bold")
        fecha = ui.input("Fecha", value="Hoy").classes("w-48")
        alumnos = listar_alumnos()
        estados = {}
        with ui.card().classes("w-full"):
            for a in alumnos:
                with ui.row().classes("w-full items-center"):
                    ui.label(f'{a["apellido"]}, {a["nombre"]} · {a["curso"] or "-"}').classes("flex-1")
                    estados[a["id"]] = ui.select(["PRESENTE","AUSENTE","JUSTIFICADO"], value="PRESENTE").classes("w-40")
            def guardar():
                for a in alumnos:
                    registrar_asistencia(a["id"], estados[a["id"]].value)
                ui.notify("Asistencia registrada", type="positive")
            ui.button("Guardar asistencia", icon="save", on_click=guardar).classes("mt-4")

def notas_view():
    c = layout("Notas y Calificaciones")
    with c:
        ui.label("Registrar y consultar notas").classes("text-3xl font-bold")
        alumnos = listar_alumnos()
        alumno = ui.select({a["id"]: f'{a["apellido"]}, {a["nombre"]}' for a in alumnos}, label="Alumno").classes("w-full")
        materia = ui.input("Materia", placeholder="Matemática").classes("w-full")
        periodo = ui.select(["1° Trimestre","2° Trimestre","3° Trimestre"], value="1° Trimestre", label="Período").classes("w-full")
        nota = ui.number("Nota", min=0, max=10, step=0.1).classes("w-full")
        def guardar():
            if not alumno.value or not materia.value or nota.value is None:
                ui.notify("Complete todos los campos", type="warning")
                return
            registrar_nota(alumno.value, materia.value, periodo.value, float(nota.value))
            ui.notify("Nota registrada", type="positive")
            tabla.refresh()
        ui.button("Guardar nota", icon="save", on_click=guardar)

        @ui.refreshable
        def tabla():
            with ui.card().classes("w-full mt-4"):
                ui.label("Notas registradas").classes("text-xl font-bold")
                rows = [{"Alumno": f'{n["apellido"]}, {n["nombre"]}', "Materia":n["materia"], "Período":n["periodo"], "Nota":n["nota"]} for n in listar_notas()]
                ui.table(columns=[
                    {"name":"Alumno","label":"Alumno","field":"Alumno"},
                    {"name":"Materia","label":"Materia","field":"Materia"},
                    {"name":"Período","label":"Período","field":"Período"},
                    {"name":"Nota","label":"Nota","field":"Nota"},
                ], rows=rows).classes("w-full")
        tabla()

def formulario_curso(refrescar, curso=None):
    with ui.dialog() as dialog:
        with ui.card().classes("w-[520px]"):
            ui.label("Editar curso" if curso else "Agregar nuevo curso").classes("text-2xl font-bold")
            nombre = ui.input("Nombre", value=curso["nombre"] if curso else "").classes("w-full")
            division = ui.input("División", value=curso["division"] if curso else "").classes("w-full")
            with ui.row().classes("w-full"):
                turno = ui.select(["Mañana", "Tarde", "Noche"], value=curso["turno"] if curso else "Mañana", label="Turno").classes("flex-1")
                anio = ui.number("Año", value=curso["anio"] if curso else 1, min=1, max=7, step=1).classes("flex-1")

            def guardar():
                if not nombre.value or not division.value or anio.value is None:
                    ui.notify("Nombre, división y año son obligatorios", type="warning")
                    return
                try:
                    if curso:
                        actualizar_curso(curso["id"], nombre.value, division.value, turno.value, int(anio.value))
                    else:
                        crear_curso(nombre.value, division.value, turno.value, int(anio.value))
                    dialog.close()
                    refrescar()
                    ui.notify("Curso guardado correctamente", type="positive")
                except Exception as e:
                    ui.notify(f"Error: {e}", type="negative")

            with ui.row().classes("justify-end w-full"):
                ui.button("Cancelar", on_click=dialog.close).props("flat")
                ui.button("Guardar curso", icon="save", on_click=guardar)
    dialog.open()

def cursos_view():
    c = layout("Gestión de Cursos")
    with c:
        with ui.row().classes("w-full items-center"):
            ui.label("Cursos").classes("text-3xl font-bold")
            ui.space()
            ui.button("Nuevo curso", icon="add", on_click=lambda: formulario_curso(refrescar)).classes("bg-blue-600 text-white")

        buscador = ui.input("Buscar por nombre, división o turno").classes("w-full mt-4")
        cont = ui.column().classes("w-full")

        def refrescar():
            cont.clear()
            texto = (buscador.value or "").lower()
            cursos = [curso for curso in listar_cursos() if texto in f'{curso["nombre"]} {curso["division"]} {curso["turno"]} {curso["anio"]}'.lower()]
            with cont:
                rows = [{"id": curso["id"], "Curso": curso["nombre"], "División": curso["division"], "Turno": curso["turno"], "Año": curso["anio"]} for curso in cursos]
                ui.table(columns=[
                    {"name": "Curso", "label": "Curso", "field": "Curso"},
                    {"name": "División", "label": "División", "field": "División"},
                    {"name": "Turno", "label": "Turno", "field": "Turno"},
                    {"name": "Año", "label": "Año", "field": "Año"},
                ], rows=rows).classes("w-full")
                with ui.row().classes("gap-2 mt-2"):
                    for curso in cursos:
                        ui.button(f'Editar {curso["nombre"]} {curso["division"]}', icon="edit", on_click=lambda curso=curso: formulario_curso(refrescar, curso)).props("outline")
                        ui.button(f'Eliminar {curso["nombre"]} {curso["division"]}', icon="delete", color="negative", on_click=lambda curso=curso: borrar(curso)).props("outline")

        def borrar(curso):
            eliminar_curso(curso["id"])
            ui.notify("Curso eliminado", type="positive")
            refrescar()

        buscador.on_value_change(lambda e: refrescar())
        refrescar()

@ui.page("/login")
def login_page():
    login_view()

@ui.page("/")
def home():
    if guard(): dashboard()

@ui.page("/alumnos")
def alumnos_page():
    if guard(): alumnos_view()

@ui.page("/asistencia")
def asistencia_page():
    if guard(): asistencia_view()

@ui.page("/notas")
def notas_page():
    if guard(): notas_view()

@ui.page("/cursos")
def cursos_page():
    if guard(): cursos_view()

ui.run(title="SRM - Sistema de Registro Escolar", port=8080, reload=False, storage_secret="srm-secret-2026")
