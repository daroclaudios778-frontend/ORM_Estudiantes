# SRM - Sistema de Registro Escolar

Versión integrada con:
- Login y roles
- Dashboard estilo SRM
- Alta, edición, búsqueda y eliminación lógica de alumnos
- Registro de asistencia
- Registro y consulta de notas
- SQLite3

## Ejecutar

Windows:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abrir: http://localhost:8080

Usuario inicial:
- Usuario: admin
- Contraseña: admin123

## Próximas etapas
- Cursos y divisiones
- Docentes
- Materias
- Reportes PDF/Excel
- Boletines
- Permisos completos por rol
- Contraseñas con hash seguro
- Ficha de salud del alumno
