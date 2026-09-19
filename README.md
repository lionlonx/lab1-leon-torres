# Laboratorio 1 — GitHub, Docker y API REST

## Integrantes
- Santiago León Alba — lionlonx
- Julian Camilo Torres Cañón — camilotorres0413

## Descripción
API REST sencilla para gestionar notas de trabajo de un equipo (`team-notes-api`).
Permite crear, consultar, actualizar y eliminar notas, cada una con título,
contenido, autor y fecha de creación.

## Tecnologías
- Python 3.12
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL 16
- Docker / Docker Compose

## Estrategia de creación de la tabla
La tabla `notes` se crea automáticamente al iniciar la aplicación mediante
`Base.metadata.create_all()` de SQLAlchemy (ver `app/database.py` y el evento
`startup` en `app/main.py`). No se usa un script SQL externo ni migraciones.

## Endpoints

| Método | Ruta          | Descripción                     |
|--------|---------------|----------------------------------|
| GET    | /health       | Estado de la API                |
| GET    | /notes        | Lista todas las notas           |
| GET    | /notes/{id}   | Consulta una nota por id        |
| POST   | /notes        | Crea una nota                   |
| PUT    | /notes/{id}   | Actualiza una nota existente    |
| DELETE | /notes/{id}   | Elimina una nota existente      |

## Cómo ejecutar

1. Copiar el archivo de variables de entorno:

   ```bash
   cp .env.example .env
   ```

2. Editar `.env` y cambiar al menos `DB_PASSWORD`.

3. Levantar los servicios:

   ```bash
   docker compose up --build
   ```

4. La API queda disponible en `http://localhost:8000` (o el puerto definido en
   `APP_PORT`). Documentación interactiva en `http://localhost:8000/docs`.

## Pruebas rápidas con curl

```bash
curl http://localhost:8000/health

curl http://localhost:8000/notes

curl -X POST http://localhost:8000/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Reunión","content":"Definir alcance del sprint","author":"Ana"}'

curl http://localhost:8000/notes/1

curl -X PUT http://localhost:8000/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Reunión (actualizada)","content":"Alcance definido","author":"Ana"}'

curl -X DELETE http://localhost:8000/notes/1
```

## Verificar persistencia

```bash
docker compose down
docker compose up
curl http://localhost:8000/notes
```

Las notas creadas antes de `docker compose down` deben seguir apareciendo,
gracias al volumen `team_notes_data`.

> No usar `docker compose down -v` antes de verificar la persistencia: ese
> comando elimina el volumen y los datos.
