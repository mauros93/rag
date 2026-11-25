# Session sirve para gestionar la conexión con la base de datos
# select se usa para hacer las consultas sql
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import InvalidCredentialsError
from app.core.security import create_access_token, verify_password
from app.models.user_model import User


class AuthService:
    """Coordina la autenticación de usuarios.

    Usa la sesión de base de datos para localizar al usuario y las utilidades
    de seguridad para verificar la contraseña y firmar el token JWT. Cuando
    las credenciales no son válidas lanza ``InvalidCredentialsError``; la
    capa HTTP lo traduce a una respuesta 401.
    """

    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(
        self,
        email: str,
        password: str
    ) -> str:
        """Valida las credenciales y devuelve un token de acceso JWT.

        Lanza ``InvalidCredentialsError`` si el usuario no existe o la
        contraseña no coincide. El manejador registrado en ``app.main``
        traduce ese error a HTTP 401.
        """

        statement = select(User).where(User.email == email)

        user = self.db.scalars(statement).first()

        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        access_token = create_access_token(
            subject=user.id
        )

        return access_token

    