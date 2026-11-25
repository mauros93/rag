# Session representa una sesión de trabajo con SQLAlchemy.
from sqlalchemy.orm import Session

from app.core.exceptions import (
    EmailAlreadyRegisteredError,
    NullFieldError,
    UserNotFoundError,
)

# Genera el hash seguro de la contraseña con Argon2id.
from app.core.security import hash_password

# User es el modelo ORM que representa la tabla users.
from app.models.user_model import User, UserRole

# Repository encapsula las operaciones de acceso a datos.
from app.repositories.user_repository import UserRepository

# UserIn, User valida los datos recibidos desde el cliente.
from app.schemas.user_schema import UserIn, UserUpdate


class UserService:
    """Contiene la lógica de negocio relacionada con los usuarios.

    Coordina las operaciones a través de ``UserRepository`` y lanza
    excepciones de dominio como ``UserNotFoundError`` o
    ``EmailAlreadyRegisteredError``. La capa HTTP las traduce a respuestas
    concretas mediante los manejadores de ``app.main``.
    """

    def __init__(self, db: Session):
        # Construimos el repositorio con la sesión recibida desde el router.
        self.user_repository = UserRepository(db)

    def create_user(self, user_data: UserIn) -> User:
        """
        Registra un usuario nuevo.
        """

        

        # Comprobamos que el correo no esté registrado.
        existing_user = self.user_repository.get_by_email(user_data.email)

        if existing_user:
            raise EmailAlreadyRegisteredError()

        hashed_password = hash_password(user_data.password)

        # Generamos el hash de la contraseña antes de almacenarla.
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=hashed_password,
            role=UserRole.USER
        )

        return self.user_repository.create(new_user)

    def get_user_by_id(self, user_id: int) -> User:
        """
        Busca un usuario por su identificador.
        """

        user = self.user_repository.get_by_id(user_id)

        # Si el repositorio no encuentra el usuario, lanzamos el error de
        # dominio que la capa HTTP traduce a un 404.
        if user is None:
            raise UserNotFoundError()

        return user

    def get_all_users(self, skip, limit) -> list[User]:
        """
        Recupera usuarios utilizando paginación.
        """

        return self.user_repository.get_all(
            skip=skip,
            limit=limit
        )

    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        # Comprueba que el usuario exista antes de modificarlo.
        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        # Obtiene únicamente los campos enviados por el cliente.
        update_data = user_data.model_dump(exclude_unset=True)

        # Evita que se envíen valores nulos para estos campos.
        for field, value in update_data.items():
            if value is None:
                raise NullFieldError(field)

        # Comprueba que el nuevo correo no pertenezca a otro usuario.
        if "email" in update_data:
            existing_user = self.user_repository.get_by_email(update_data["email"])

            if existing_user and existing_user.id != user_id:
                raise EmailAlreadyRegisteredError()

        # Modifica únicamente los atributos recibidos.
        for field, value in update_data.items():
            setattr(user, field, value)

        return self.user_repository.update(user)


    def delete_user(self, user_id: int):
        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        self.user_repository.delete(user)


    def update_user_role(
        self,
        user_id: int,
        new_role: UserRole
    ) -> User:

        user = self.user_repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError()

        user.role = new_role

        return self.user_repository.update(user)

    