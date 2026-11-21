# Bitácora — Blog web con Django

Proyecto final del curso de Python. Un blog en español donde los visitantes leen y buscan publicaciones, y los usuarios registrados comparten sus propias historias.

**Autor:** brunastix (Bruno). [Perfil de GitHub](https://github.com/brunastix).

## Tecnologías

Python 3.12 (recomendado), Django 5.2 LTS, SQLite, Pillow, python-decouple, HTML y CSS responsive sin servicios externos. Las versiones instaladas se fijan en `requirements.txt`.

## Funcionalidades

- Listado paginado, detalle y búsqueda por título o contenido.
- Crear, editar y eliminar publicaciones desde la web.
- Imágenes opcionales JPG, PNG y WEBP de hasta 5 MB; presentación alternativa sin imagen.
- Registro con validación de contraseña, login y logout mediante POST.
- Perfil privado con nombre, fecha de alta y publicaciones propias. No incluye edición ni avatar.
- Protección en las vistas: solo el autor puede modificar o eliminar sus publicaciones. Un usuario ajeno recibe 404; un visitante es redirigido al login.
- Panel administrativo opcional.

## Instalación desde cero

Requisitos: Python 3.12 y Git. Cloná la URL del repositorio y entrá en la carpeta que creó Git. Si descargaste el código para probarlo antes de publicarlo, entrá en la carpeta que contiene `manage.py`.

En Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver
```

Si PowerShell bloquea la activación, usá `.venv\Scripts\python.exe` en lugar de `python` en los comandos restantes, sin cambiar políticas del sistema.

En Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Abrí http://127.0.0.1:8000/. La base comienza vacía: creá una cuenta desde **Crear cuenta**, elegí **Escribir** y guardá una publicación con una imagen de tu computadora. No se necesitan cuentas ni contraseñas predefinidas.

No se versionan `db.sqlite3` ni `media/`: `migrate` crea la base y las cargas desde la web crean las imágenes. Si no existe `.env`, se usa `.env.example` exclusivamente como configuración local de desarrollo.

Para probar el administrador, ejecutá `python manage.py createsuperuser` y abrí http://127.0.0.1:8000/admin/. El CRUD solicitado funciona sin usar el administrador.

## Configuración y seguridad

`.env.example` contiene una clave pública de ejemplo que **solo sirve para desarrollo**. Nunca publiques `.env`. Las variables del entorno tienen prioridad sobre el archivo.

- `SECRET_KEY`: generar una clave privada para un despliegue con `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`.
- `DEBUG`: `True` en desarrollo; `False` fuera del entorno local.
- `ALLOWED_HOSTS`: dominios permitidos separados por comas, sin protocolo.

Las rutas se construyen con `BASE_DIR`. `MEDIA_ROOT` y `MEDIA_URL` sirven archivos subidos en desarrollo; `STATIC_URL` y `STATICFILES_DIRS` sirven el CSS. Con `DEBUG=False`, configurar HTTPS, servidor WSGI, dominio y servicios de estáticos/media; ejecutar `collectstatic` y revisar `check --deploy`. El servidor de desarrollo no es un servidor de producción. La configuración rechaza la clave de ejemplo con `DEBUG=False` y habilita cookies seguras y redirección HTTPS.

Se usan CSRF, escape HTML, ORM y contraseñas hasheadas de Django. Los archivos reciben nombres aleatorios y se validan como imágenes. Esta entrega local no incorpora limitación de intentos de login. Al reemplazar o eliminar imágenes, Django conserva archivos anteriores en disco; antes de un despliegue sostenido se necesita una tarea de limpieza de archivos huérfanos y límites de carga en el servidor.

## Verificación automatizada

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Las pruebas utilizan una base temporal y una carpeta temporal para imágenes. Comprueban CRUD vía HTTP, imágenes válidas e inválidas, permisos, registro/login/logout, perfil, CSRF, escape HTML, búsquedas y redirecciones.

## Recorrido manual antes de entregar

1. Como visitante, leer listado y detalle, buscar un texto existente y otro inexistente.
2. Entrar en `/posts/nuevo/` y `/cuentas/perfil/` sin sesión: deben pedir login.
3. Registrar una cuenta. Crear un post sin imagen y otro con PNG/JPG; abrir ambos.
4. Editar título, contenido e imagen. Quitar una imagen y comprobar el detalle.
5. Entrar en eliminar y cancelar; luego confirmar la eliminación.
6. Cerrar sesión, volver a ingresar y revisar el perfil.
7. Crear otra cuenta e intentar abrir la URL de edición de un post ajeno: debe dar 404.
8. Tras publicar, abrir el repositorio sin sesión de GitHub, clonarlo en otra carpeta y repetir la instalación.

## Estructura

`config/`: configuración y rutas globales. `blog/`: modelo, formularios, vistas, rutas, migración y pruebas. `templates/`: interfaz. `static/`: estilos. `requirements.txt`: dependencias reproducibles.

## Publicación y entrega

Crear un repositorio **público** en GitHub sin inicializarlo con README (este proyecto ya lo incluye). Conectarlo con `git remote add origin URL_DEL_REPOSITORIO` y subir con `git push -u origin main`. No introducir tokens en los archivos o comandos guardados.

Antes de enviar a Ticher, verificar el acceso público y que el último commit remoto coincida con el local. Entregar la URL directa del repositorio, no un ZIP ni el perfil. El historial local registra etapas reales del desarrollo, sin fechas inventadas.
