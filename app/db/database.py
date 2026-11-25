
# create_engine: crea el motor que administra las conexiones
# entre nuestra aplicación y PostgreSQL.
from sqlalchemy import create_engine

# sessionmaker: permite crear sesiones para ejecutar operaciones
# sobre la base de datos.
from sqlalchemy.orm import sessionmaker

# Importamos la configuración centralizada.
from app.core.config import settings


# --------------------------------------------------
# 1. URL DE CONEXIÓN
# --------------------------------------------------

# Construimos la dirección que SQLAlchemy utilizará
# para conectarse a PostgreSQL.
#
# Formato:
# postgresql+psycopg://usuario:contraseña@host:puerto/base_datos
#
# localhost: porque FastAPI se ejecuta fuera de Docker.
# Más adelante, si FastAPI también se ejecuta en Docker,
# cambiaremos localhost por el nombre del servicio: db.

DATABASE_URL = (
    f"postgresql+psycopg://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@localhost:5432/"
    f"{settings.POSTGRES_DB}"
)


# --------------------------------------------------
# 2. MOTOR DE CONEXIÓN
# --------------------------------------------------

# create_engine configura el mecanismo de comunicación
# entre SQLAlchemy y PostgreSQL.
#
# No crea las tablas ni abre una conexión permanente.
# Administra las conexiones cuando la aplicación las necesita.
#
# echo=True muestra las consultas SQL en la terminal.
# Es útil durante el desarrollo para entender qué ejecuta SQLAlchemy.

engine = create_engine(
    DATABASE_URL,
    echo=settings.DEBUG
)


# --------------------------------------------------
# 3. FÁBRICA DE SESIONES
# --------------------------------------------------

# sessionmaker es una fábrica que crea sesiones.
#
# Eficiencia: En lugar de abrir la base de datos, escribir un dato y cerrar (repetidamente),
# la sesión agrupa múltiples cambios y los envía en una sola operación.
#
# bind=engine: indica qué motor utilizarán las sesiones.
# autoflush=False: evita enviar cambios pendientes automáticamente
# antes de cada consulta.
# autocommit=False: exige confirmar explícitamente las transacciones.

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# --------------------------------------------------
# 4. DEPENDENCIA PARA OBTENER SESIONES
# --------------------------------------------------

# Esta función proporciona una sesión de base de datos
# a los endpoints que la necesiten.
#
# yield entrega la sesión al endpoint.
# finally garantiza que se cierre cuando termine la operación,
# incluso si ocurre un error.

def get_db():

    # Creamos una nueva sesión.
    db = SessionLocal()

    try:
        # Entregamos la sesión al componente que la solicitó.
        yield db

    finally:
        # Cerramos la sesión para liberar los recursos.
        db.close()
