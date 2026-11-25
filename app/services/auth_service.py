from app.core.exceptions import InvalidCredentialsError
from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRepository


class AuthService:
    """Coordina la autenticación de usuarios.

    Usa el repositorio para localizar al usuario y las utilidades de
    seguridad para verificar la contraseña y firmar el token JWT. Cuando las
    credenciales no son válidas lanza ``InvalidCredentialsError``; la capa
    HTTP lo traduce a una respuesta 401.
    """

    def __init__(self, user_repository: UserRepository):
        # El repositorio se inyecta desde la capa de dependencias.
        self.user_repository = user_repository

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

        user = self.user_repository.get_by_email(email)

        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        access_token = create_access_token(
            subject=user.id
        )

        return access_token

    