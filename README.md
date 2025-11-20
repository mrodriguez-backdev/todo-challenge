# Invera ToDo-List Challenge (Python/Django Jr-SSr)

El propósito de esta prueba es conocer tu capacidad para crear una pequeña aplicación funcional en un límite de tiempo. A continuación, encontrarás las funciones, los requisitos y los puntos clave que debés tener en cuenta durante el desarrollo.

## Qué queremos que hagas:

- El Challenge consiste en crear una aplicación web sencilla que permita a los usuarios crear y mantener una lista de tareas.
- La entrega del resultado será en un nuevo fork de este repo y deberás hacer una pequeña demo del funcionamiento y desarrollo del proyecto ante un super comité de las más grandes mentes maestras de Invera, o a un par de devs, lo que sea más fácil de conseguir.
- Podes contactarnos en caso que tengas alguna consulta.

## Objetivos:

El usuario de la aplicación tiene que ser capaz de:

- Autenticarse
- Crear una tarea
- Eliminar una tarea
- Marcar tareas como completadas
- Poder ver una lista de todas las tareas existentes
- Filtrar/buscar tareas por fecha de creación y/o por el contenido de la misma

## Qué evaluamos:

- Desarrollo utilizando Python, Django. No es necesario crear un Front-End, pero sí es necesario tener una API que permita cumplir con los objetivos de arriba.
- Uso de librerías y paquetes estandares que reduzcan la cantidad de código propio añadido.
- Calidad y arquitectura de código. Facilidad de lectura y mantenimiento del código. Estándares seguidos.
- [Bonus] Manejo de logs.
- [Bonus] Creación de tests (unitarias y de integración)
- [Bonus] Unificar la solución propuesta en una imagen de Docker por repositorio para poder ser ejecutada en cualquier ambiente (si aplica para full stack).

## Requerimientos de entrega:

- Hacer un fork del proyecto y pushearlo en github. Puede ser privado.
- La solución debe correr correctamente.
- El Readme debe contener todas las instrucciones para poder levantar la aplicación, en caso de ser necesario, y explicar cómo se usa.
- Disponibilidad para realizar una pequeña demo del proyecto al finalizar el challenge.
- Tiempo para la entrega: Aproximadamente 7 días.

---

## 🚀 Setup y Ejecución del Proyecto

### Requisitos Previos
- Docker
- Docker Compose

### Instalación y Ejecución

#### 1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd todo-challenge
```

#### 2. **Levantar los servicios con Docker Compose**
```bash
docker compose up --build
```

**Esto automáticamente:**
- ✅ Construye la imagen de Django
- ✅ Levanta PostgreSQL en el puerto **5434**
- ✅ Ejecuta las migraciones de base de datos
- ✅ Crea un superusuario admin automáticamente
- ✅ Inicia el servidor de desarrollo en el puerto **8002**

#### 3. **Acceder a la aplicación**

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **API Base** | http://localhost:8002/api/ | Endpoint base de la API |
| **Health Check** | http://localhost:8002/api/health/ | Verifica estado de la API |
| **Django Admin** | http://localhost:8002/admin/ | Panel de administración |
| **Swagger UI** | http://localhost:8002/api/docs/ | Documentación interactiva de la API |
| **ReDoc** | http://localhost:8002/api/redoc/ | Documentación alternativa |

#### 4. **Credenciales del superusuario**

Por defecto, se crea automáticamente un superusuario:
- **Usuario**: `admin`
- **Contraseña**: `admin123`
- **Email**: `admin@example.com`

Puedes cambiar estas credenciales en `docker-compose.yml` (variables de entorno).

---

## 📊 Cargar Datos Iniciales

El proyecto incluye un comando para cargar datos de prueba (4 estados y 10 tareas de ejemplo):

```bash
docker compose exec web python manage.py load_initial_data
```

**Datos que se cargan:**

**Status:**
- Por Hacer (gris)
- En Progreso (azul)
- Completado (verde)
- Bloqueado (rojo)

**Tareas (10 ejemplos):**
- Crear función de suma
- Implementar bucle for
- Declarar variables
- Crear clase Usuario
- Escribir comentarios en código
- Hacer commit en git
- Revisar pull request
- Actualizar dependencias
- Corregir error de sintaxis
- Agregar validación de datos

**Nota:** El comando es idempotente, puedes ejecutarlo múltiples veces sin duplicar datos.

---

## 🧪 Ejecutar Tests

El proyecto incluye **41 tests de integración** que cubren:
- Autenticación JWT
- CRUD de Status
- CRUD de Tasks
- Filtros y búsquedas
- Validaciones

### Ejecutar todos los tests:
```bash
docker compose exec web python manage.py test
```

### Ejecutar tests específicos:

```bash
# Tests de autenticación JWT
docker compose exec web python manage.py test api.tests.test_auth

# Tests de Status (GET)
docker compose exec web python manage.py test api.tests.test_status

# Tests de Task GET
docker compose exec web python manage.py test api.tests.test_task_get

# Tests de Task POST
docker compose exec web python manage.py test api.tests.test_task_post

# Tests de Task DELETE
docker compose exec web python manage.py test api.tests.test_task_delete
```

### Ejecutar un test individual:
```bash
docker compose exec web python manage.py test api.tests.test_task_post.TaskPostTestCase.test_create_task_success
```

### Ver tests con más detalle:
```bash
docker compose exec web python manage.py test --verbosity=2
```

---

## 📡 Endpoints de la API

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/auth/token/` | Obtener token JWT |
| POST | `/api/auth/token/refresh/` | Refrescar token JWT |

**Ejemplo: Obtener token**
```bash
curl -X POST http://localhost:8002/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Status

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/status/` | Listar todos los estados |
| POST | `/api/status/` | Crear un nuevo estado |
| GET | `/api/status/{id}/` | Obtener un estado específico |
| PUT | `/api/status/{id}/` | Actualizar un estado completo (requiere todos los campos) |
| DELETE | `/api/status/{id}/` | Eliminar un estado |

### Tasks

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tasks/` | Listar todas las tareas |
| POST | `/api/tasks/` | Crear una nueva tarea |
| GET | `/api/tasks/{id}/` | Obtener una tarea específica |
| PUT | `/api/tasks/{id}/` | Actualizar una tarea completa (requiere todos los campos) |
| DELETE | `/api/tasks/{id}/` | Eliminar una tarea |
| POST | `/api/tasks/mark-as-complete/` | Marcar múltiples tareas como completadas |

### Filtros y Búsqueda (Tasks)

```bash
# Filtrar por status
GET /api/tasks/?status=1

# Buscar por nombre o contenido
GET /api/tasks/?search=función

# Filtrar por fecha de creación
GET /api/tasks/?created_at__gte=2025-01-01

# Ordenar por nombre
GET /api/tasks/?ordering=name

# Combinar filtros
GET /api/tasks/?status=1&search=función&ordering=-created_at
```

**Ejemplo: Crear una tarea**
```bash
curl -X POST http://localhost:8002/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nueva tarea",
    "content": "Descripción de la tarea",
    "status": 1
  }'
```

**Ejemplo: Marcar tareas como completadas**
```bash
curl -X POST http://localhost:8002/api/tasks/mark-as-complete/ \
  -H "Content-Type: application/json" \
  -d '{"task_ids": [1, 2, 3]}'
```

---

## 🛠️ Comandos Útiles

### Docker Compose

```bash
# Detener los servicios
docker compose down

# Ver logs en tiempo real
docker compose logs -f web

# Reiniciar solo el servicio web
docker compose restart web

# Reconstruir las imágenes
docker compose up --build

# Eliminar volúmenes (resetear DB)
docker compose down -v
```

### Django Management Commands

```bash
# Acceder al shell de Django
docker compose exec web python manage.py shell

# Crear migraciones
docker compose exec web python manage.py makemigrations

# Ejecutar migraciones
docker compose exec web python manage.py migrate

# Cargar datos iniciales
docker compose exec web python manage.py load_initial_data

# Crear superusuario manualmente
docker compose exec web python manage.py create_superuser_if_none_exists
```

---

## 📁 Estructura del Proyecto

```
todo-challenge/
├── api/                              # App principal de la API
│   ├── management/                   # Comandos personalizados
│   │   └── commands/
│   │       ├── create_superuser_if_none_exists.py
│   │       └── load_initial_data.py
│   ├── models/                       # Modelos de datos
│   │   ├── status.py                 # Modelo Status
│   │   └── task.py                   # Modelo Task
│   ├── serializers/                  # Serializers de DRF
│   │   ├── health/
│   │   ├── status/
│   │   └── task/
│   │       ├── task.py               # TaskSerializer
│   │       └── mark_complete.py      # MarkTasksAsCompleteSerializer
│   ├── views/                        # ViewSets y vistas
│   │   ├── health/
│   │   ├── status/
│   │   └── task/
│   │       ├── task.py               # TaskViewSet (CRUD)
│   │       └── mark_complete.py      # mark_tasks_as_complete
│   ├── tests/                        # Tests de integración
│   │   ├── test_auth.py              # Tests de autenticación JWT
│   │   ├── test_status.py            # Tests de Status
│   │   ├── test_task_get.py          # Tests de GET Task
│   │   ├── test_task_post.py         # Tests de POST Task
│   │   └── test_task_delete.py       # Tests de DELETE Task
│   ├── migrations/                   # Migraciones de base de datos
│   └── urls.py                       # Configuración de rutas
├── todo_challenge/                   # Configuración del proyecto
│   ├── settings.py                   # Configuración de Django
│   └── urls.py                       # URLs principales
├── Dockerfile                        # Imagen Docker de Django
├── docker-compose.yml                # Orquestación de servicios
├── entrypoint.sh                     # Script de inicio automático
├── requirements.txt                  # Dependencias Python
└── README.md                         # Este archivo
```

---

## 🔧 Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.12 | Lenguaje de programación |
| **Django** | 4.2.26 LTS | Framework web |
| **Django REST Framework** | 3.16.1 | API REST |
| **PostgreSQL** | 15-alpine | Base de datos |
| **djangorestframework-simplejwt** | 5.5.1 | Autenticación JWT |
| **drf-spectacular** | 0.29.0 | Documentación OpenAPI/Swagger |
| **django-filter** | 24.3 | Filtros avanzados |
| **Docker & Docker Compose** | - | Containerización |

---

## 📝 Notas de Desarrollo

### Puertos utilizados
- **PostgreSQL**: 5434 (externo) → 5432 (interno)
- **Django**: 8002 (externo) → 8000 (interno)

### Variables de entorno (docker-compose.yml)
Puedes personalizar estas variables en el archivo `docker-compose.yml`:

```yaml
environment:
  - DJANGO_SUPERUSER_USERNAME=admin
  - DJANGO_SUPERUSER_EMAIL=admin@example.com
  - DJANGO_SUPERUSER_PASSWORD=admin123
  - DB_NAME=todo_challenge
  - DB_USER=postgres
  - DB_PASSWORD=postgres
```

### Características implementadas

✅ Autenticación con JWT
✅ CRUD completo de Tasks y Status
✅ Filtrado por status, fecha y búsqueda de texto
✅ Endpoint personalizado para marcar tareas como completadas
✅ Validación de tareas ya completadas
✅ Documentación interactiva con Swagger/ReDoc
✅ 41 tests de integración
✅ Datos iniciales cargables con comando
✅ Superusuario creado automáticamente
✅ Proyecto completamente dockerizado

---

## 🐛 Troubleshooting

**Error: Puerto 5434 o 8002 ya en uso**
```bash
# Ver qué proceso está usando el puerto
sudo lsof -i :5434
sudo lsof -i :8002

# Detener servicios existentes
docker compose down
```

**Error: Permisos de Docker**
```bash
# Agregar tu usuario al grupo docker
sudo usermod -aG docker $USER
# Luego cerrar sesión y volver a iniciar
```

**Resetear la base de datos completamente**
```bash
docker compose down -v
docker compose up --build
```
