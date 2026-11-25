from fastapi import FastAPI

from app.db.database import get_db

# Importamos la configuración centralizada.
from app.core.config import settings

# Importamos el router de usuario
from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router


# --------------------------------------------------
# 1. CREACIÓN DE LA APLICACIÓN
# --------------------------------------------------

# Creamos la instancia principal de FastAPI.
#
# Esta instancia representa nuestra API.
# Sobre ella registraremos los endpoints, routers,
# middlewares y otras configuraciones.

app = FastAPI(

    # Nombre que aparecerá en la documentación automática.
    title=settings.APP_NAME,

    # Versión de nuestra API.
    version=settings.APP_VERSION,

    # Activa o desactiva el modo de depuración.
    debug=settings.DEBUG
)


app.include_router(user_router)
app.include_router(auth_router)


# --------------------------------------------------
# 2. ENDPOINT PRINCIPAL
# --------------------------------------------------

@app.get("/")
def entry_point():
    return {"msg": "¡Bienvenido a la API!"}



