# Depends: Inyección de dependencias automática antes de ejecutar el endpoint.
# HTTPException y status: Permiten cortar la petición y devolver códigos HTTP (ej. 401).
from fastapi import Depends, HTTPException, status

# HTTPBearer: Extrae el header "Authorization: Bearer <token>" y activa el botón en Swagger.
# HTTPAuthorizationCredentials: Estructura el header en `.scheme` ("Bearer") y `.credentials` (el token).
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# select: Constructor de consultas de SQLAlchemy 2.0.
# Session: Representa una sesión activa con la base de datos.
from sqlalchemy import select
from sqlalchemy.orm import Session

# jwt: Módulo principal de PyJWT para firmar (encode) y verificar/leer (decode) tokens.
import jwt

# InvalidTokenError: Excepción base de PyJWT; atrapa tokens expirados (ExpiredSignatureError),
#                    firmas alteradas (InvalidSignatureError) o formatos corruptos (DecodeError).
from jwt.exceptions import InvalidTokenError

from app.db.database import get_db
from app.core.config import settings
from app.models.user_model import User, UserRole


# Exige el header "Authorization: Bearer <token>" en cada ruta que use esta dependencia
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:

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

    # Verifica que el usuario dueño del token siga existiendo en la base de datos
    statement = select(User).where(User.id == user_id)
    user = db.scalars(statement).first()

    if user is None:
        raise credentials_exception

    return user



def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:

    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action"
        )

    return current_user