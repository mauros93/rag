
# Importamos PasswordHash desde pwdlib.
# Esta clase proporciona una interfaz para generar y verificar
# hashes de contraseñas utilizando diferentes algoritmos.
from pwdlib import PasswordHash


# Libreria para trabajar con tokens JWT
import jwt


from datetime import datetime, timedelta, timezone


from app.core.config import settings




# Creamos una instancia de PasswordHash utilizando la configuración
# recomendada por la biblioteca.
#
# Como instalamos pwdlib con el soporte de Argon2,
# la configuración recomendada utiliza Argon2id.
#
# Esta instancia se reutilizará en toda la aplicación.
# No necesitamos crear una instancia por cada usuario.
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Genera un hash seguro a partir de una contraseña.

    Recibe:
        password: contraseña original enviada por el usuario.

    Retorna:
        Una cadena con el hash generado por Argon2id.

    Importante:
        La contraseña original no se almacena ni se puede
        recuperar directamente a partir del hash.
    """

    # Argon2id genera automáticamente una sal aleatoria,
    # aplica sus parámetros de coste y produce el hash.
    #
    # El resultado incluye la información necesaria para
    # verificar posteriormente la contraseña.
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Comprueba si una contraseña coincide con un hash almacenado.

    Recibe:
        plain_password: contraseña original proporcionada
                        durante el inicio de sesión.

        hashed_password: hash previamente almacenado
                         en PostgreSQL.

    Retorna:
        True si la contraseña coincide.
        False si la contraseña no coincide.
    """

    # pwdlib obtiene del hash almacenado la sal y los parámetros
    # necesarios para repetir el proceso de verificación.
    #
    # No debemos generar un hash nuevo para comparar cadenas,
    # porque cada generación utiliza una sal aleatoria.
    return password_hash.verify(
        plain_password,
        hashed_password
    )


def create_access_token(
    subject: str | int,                 # Identificador del usuario, en este caso el id
    expires_delta: timedelta | None = None  # Tiempo opcional de duración
) -> str:

    # Si no se especificó un tiempo de expiración personalizado,
    # se toma el tiempo en minutos configurado en los settings de la app
    if expires_delta is None:
        expires_delta = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Calcula la fecha y hora exacta en que vencerá el token usando la hora actual en UTC
    expiration = datetime.now(timezone.utc) + expires_delta

    # Construye los datos (claims) que viajarán dentro del token:
    # "sub" (subject): a quién pertenece el token (convertido a texto por estándar JWT)
    # "exp" (expiration): cuándo deja de ser válido el token
    payload = {
        "sub": str(subject),
        "exp": expiration
    }

    # Genera y firma el token JWT usando la clave secreta y el algoritmo configurado (ej. HS256)
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    # Devuelve el token JWT ya generado como una cadena de texto
    return token