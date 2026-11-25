from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

# Importamos la configuración centralizada.
from app.core.config import settings
from app.core.exceptions import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    NullFieldError,
    UserNotFoundError,
)

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



# 1. EL INTERCEPTOR (Decorador)
# Le dice a FastAPI: "Si ocurre un UserNotFoundError en cualquier endpoint,
# detén todo y pásale el control a esta función en lugar de devolver un error 500".
@app.exception_handler(UserNotFoundError)
async def handle_user_not_found(
    # 2. LOS PARÁMETROS (Lo que FastAPI te entrega automáticamente)
    # request: Contiene toda la info de la petición HTTP que falló (URL, headers, IP, método).
    #          Aunque no la uses adentro, FastAPI exige recibirla como primer argumento.
    request: Request,
    # exc: Es la instancia exacta del error que lanzó tu servicio (ej. raise UserNotFoundError()).
    #      Sirve por si quieres leer datos o mensajes que traiga el error por dentro.
    exc: UserNotFoundError,
) -> JSONResponse:  # 3. TIPO DE RETORNO: Avisa que devolveremos una respuesta HTTP en JSON.
    """Traduce ``UserNotFoundError`` a una respuesta HTTP 404."""

    # 4. LA TRADUCCIÓN A HTTP
    # Como estamos fuera de un router/endpoint, FastAPI no convierte diccionarios
    # automáticamente; debemos construir la respuesta web manualmente con JSONResponse.
    return JSONResponse(
        # Código de estado HTTP (404 = Recurso no encontrado)
        status_code=status.HTTP_404_NOT_FOUND,
        # Cuerpo del JSON que recibirá el frontend o cliente.
        # Se usa la llave "detail" para mantener el mismo formato de errores que usa FastAPI.
        content={"detail": "Usuario no encontrado"},
    )


@app.exception_handler(EmailAlreadyRegisteredError)
async def handle_email_already_registered(
    request: Request,
    exc: EmailAlreadyRegisteredError
) -> JSONResponse:
    """Traduce ``EmailAlreadyRegisteredError`` a una respuesta HTTP 409."""

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "El correo electrónico ya está registrado"},
    )


@app.exception_handler(InvalidCredentialsError)
async def handle_invalid_credentials(
    request: Request,
    exc: InvalidCredentialsError
) -> JSONResponse:
    """Traduce ``InvalidCredentialsError`` a una respuesta HTTP 401."""

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid email or password"},
    )


@app.exception_handler(NullFieldError)
async def handle_null_field(
    request: Request,
    exc: NullFieldError
) -> JSONResponse:
    """Traduce ``NullFieldError`` a una respuesta HTTP 422."""

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": str(exc)},
    )


app.include_router(user_router)
app.include_router(auth_router)


# --------------------------------------------------
# 2. ENDPOINT PRINCIPAL
# --------------------------------------------------

@app.get("/")
def entry_point():
    return {"msg": "¡Bienvenido a la API!"}



