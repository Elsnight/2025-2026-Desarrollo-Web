# Faustos Coffee

Tienda online academica construida con Flask para demostrar una evolucion por fases: catalogo web, persistencia en archivos, SQLite/MySQL, autenticacion, CRUD protegido y generacion de reportes PDF.

## Funcionalidades principales

- Catalogo publico con vistas en Jinja2 y Bootstrap.
- CRUD web completo de productos desde formularios HTML.
- Autenticacion con registro, login, logout y rutas protegidas con `Flask-Login`.
- Persistencia principal con SQLAlchemy sobre SQLite o MySQL.
- Exportacion del catalogo a `TXT`, `JSON` y `CSV`.
- Generacion de reporte PDF del inventario desde el panel privado.

## Estructura del proyecto

```text
faustos-coffee/
|-- app/
|   |-- forms/
|   |-- models/
|   |-- routes/
|   `-- services/
|-- data/
|-- static/
|-- templates/
|-- config.py
|-- requirements.txt
|-- run.py
`-- render.yaml
```

## Requisitos

- Python 3.10 o superior
- `pip`
- MySQL opcional si quieres probar el proyecto con ese motor

## Instalacion local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Variables de entorno

La aplicacion funciona con SQLite por defecto. Si no defines variables, se creara `data/faustos_coffee.sqlite3`.

Variables soportadas:

- `SECRET_KEY`: clave secreta de Flask.
- `DATABASE_ENGINE`: `sqlite` o `mysql`.
- `MYSQL_USER`: usuario de MySQL.
- `MYSQL_PASSWORD`: contrasena de MySQL.
- `MYSQL_HOST`: host de MySQL.
- `MYSQL_PORT`: puerto de MySQL.
- `MYSQL_DATABASE`: nombre de la base de datos.

Ejemplo para PowerShell con SQLite:

```powershell
$env:SECRET_KEY = "faustos-coffee-local"
python run.py
```

Ejemplo para PowerShell con MySQL:

```powershell
$env:SECRET_KEY = "faustos-coffee-local"
$env:DATABASE_ENGINE = "mysql"
$env:MYSQL_USER = "root"
$env:MYSQL_PASSWORD = "tu_password"
$env:MYSQL_HOST = "localhost"
$env:MYSQL_PORT = "3306"
$env:MYSQL_DATABASE = "faustos_coffee"
python run.py
```

## Ejecucion

```bash
python run.py
```

Despues abre:

- `http://127.0.0.1:5000/`
- `http://127.0.0.1:5000/productos`
- `http://127.0.0.1:5000/login`
- `http://127.0.0.1:5000/admin/productos`

## Flujo recomendado de uso

1. Registrar un usuario en `/registro`.
2. Iniciar sesion en `/login`.
3. Crear, editar y eliminar productos desde `/admin/productos`.
4. Exportar archivos planos y generar el reporte PDF del catalogo.
5. Revisar `/productos/archivos` para mostrar los archivos `TXT`, `JSON` y `CSV`.

## Preparacion para GitHub

1. Crear un repositorio nuevo en GitHub.
2. Desde la carpeta del proyecto ejecutar:

```bash
git init
git add .
git commit -m "Prepare Faustos Coffee delivery"
git branch -M main
git remote add origin <URL_DEL_REPOSITORIO>
git push -u origin main
```

3. Verificar que el repositorio incluya:
- `README.md`
- `requirements.txt`
- `render.yaml`
- carpeta `app/`
- plantillas y recursos estaticos

## Despliegue en Render

El archivo `render.yaml` deja preparada una app web Python con `gunicorn`.

Pasos:

1. Subir el proyecto a GitHub.
2. En Render, elegir `New +` -> `Blueprint`.
3. Conectar el repositorio.
4. Definir una `SECRET_KEY` segura.
5. Si vas a usar MySQL, cambiar `DATABASE_ENGINE` y completar las variables de conexion.

Nota: con SQLite el despliegue es valido para demostracion, pero para produccion conviene usar MySQL o PostgreSQL.

## Defensa del proyecto

### Arquitectura

- `routes`: reciben peticiones HTTP y renderizan vistas o redirigen.
- `forms`: validan y transforman los datos enviados desde HTML.
- `services`: concentran la logica del catalogo, archivos y PDF.
- `models`: representan `Producto`, `Usuario` y `Cliente`.
- `templates`: construyen la interfaz con Jinja2.

### Explicacion corta por capas

- La vista envia datos del formulario al backend.
- La ruta usa un formulario para validar esos datos.
- El servicio del catalogo decide como crear, editar o eliminar.
- `Inventario` usa SQLAlchemy para persistir en SQLite o MySQL.
- Luego se sincronizan archivos planos y, si se necesita, se genera el PDF.

### Puntos clave para sustentar

- Por que usar `create_app()`: permite una estructura mantenible y escalable.
- Por que usar `Flask-Login`: protege el CRUD y separa usuarios autenticados del catalogo publico.
- Por que usar SQLAlchemy: facilita cambiar de SQLite a MySQL sin reescribir todo.
- Por que mantener TXT, JSON y CSV: cumple el requisito academico de persistencia en archivos.
- Por que generar PDF: permite entregar un reporte portable del inventario actual.

## Endpoints relevantes

- `GET /`: inicio.
- `GET /productos`: catalogo publico.
- `GET /producto/<slug>`: detalle de un producto.
- `GET|POST /registro`: registro de usuarios.
- `GET|POST /login`: inicio de sesion.
- `POST /logout`: cierre de sesion.
- `GET /admin/productos`: panel CRUD protegido.
- `POST /admin/productos/crear`: crear producto.
- `POST /admin/productos/<id>/editar`: editar producto.
- `POST /admin/productos/<id>/eliminar`: eliminar producto.
- `POST /admin/productos/exportar-archivos`: regenerar TXT, JSON y CSV.
- `GET /admin/productos/reporte.pdf`: descargar reporte PDF.

## Dependencias destacadas

- `Flask`
- `Flask-Login`
- `Flask-SQLAlchemy`
- `PyMySQL`
- `reportlab`
- `gunicorn`
