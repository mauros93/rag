# Depends: Inyección de dependencias automática antes de ejecutar el endpoint.
# HTTPException y status: Permiten cortar la petición y devolver códigos HTTP (ej. 401).
# jwt: Módulo principal de PyJWT para firmar (encode) y verificar/leer (decode) tokens.
import jwt
from fastapi import Depends, HTTPException, status

# HTTPBearer: Extrae el header "Authorization: Bearer <token>" y activa el botón en Swagger.
# HTTPAuthorizationCredentials: Estructura el header en `.scheme` ("Bearer") y `.credentials` (el token).
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# InvalidTokenError: Excepción base de PyJWT; atrapa tokens expirados (ExpiredSignatureError),
#                    firmas alteradas (InvalidSignatureError) o formatos corruptos (DecodeError).
from jwt.exceptions import InvalidTokenError

# Session: Representa una sesión activa con la base de datos.
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.models.user_model import User, UserRole
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService

# Exige el header "Authorization: Bearer <token>" en cada ruta que use esta dependencia
bearer_scheme = HTTPBearer()


def get_user_repository(
    db: Session = Depends(get_db)
) -> UserRepository:
    """Proporciona un repositorio de usuarios ligado a la petición actual.

    FastAPI reutiliza la misma sesión de base de datos durante toda la
    petición, por lo que el repositorio comparte su ciclo de vida.
    """

    return UserRepository(db)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    """Proporciona un ``UserService`` con su repositorio inyectado.

    La capa HTTP no necesita conocer cómo se construyen la sesión ni el
    repositorio.
    """

    return UserService(user_repository)


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> AuthService:
    """Proporciona un ``AuthService`` con su repositorio inyectado."""

    return AuthService(user_repository)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    user_repository: UserRepository = Depends(get_user_repository)
) -> User:
    """Obtiene el usuario autenticado a partir del token Bearer.

    Decodifica y valida el JWT, extrae el identificador del usuario del
    claim ``sub`` y lo busca a través del repositorio. Lanza HTTP 401 si el
    token es inválido, expiró o el usuario ya no existe.
    """

    # El header WWW-Authenticate es requerido por el estándar HTTP al devolver 401 con Bearer
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # Extrae el string limpio del JWT sin la palabra "Bearer "
    token = credentials.credentials

    try:
        # Verifica la firma con la clave secreta, valida que no haya expirado ("exp")
        # y exige que el algoritmo coincida con la lista permitida
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # Extrae el ID del usuario ("sub") guardado al iniciar sesión
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        # Convierte el "sub" de string (estándar JWT) a entero para buscar en la BD
        user_id = int(user_id)

    except (InvalidTokenError, ValueError, TypeError):
        raise credentials_exception

    # Verifica que el usuario dueño del token siga existiendo en la base de datos.
    user = user_repository.get_by_id(user_id)

    if user is None:
        raise credentials_exception

    return user



def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """Verifica que el usuario autenticado sea administrador.

    Lanza HTTP 403 cuando el rol del usuario no es ``UserRole.ADMIN``.
    """

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )

    return current_user