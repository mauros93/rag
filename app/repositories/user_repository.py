# Este archivo abstrae la capa de datos y centraliza todas las consultas SQL 
# (CRUD) de usuarios, separando la persistencia de la lógica de negocio.


# Session representa la sesión de trabajo con la base de datos.
# select permite construir consultas SQL de forma declarativa.
from sqlalchemy import select
from sqlalchemy.orm import Session

# User representa el modelo ORM asociado a la tabla users.
from app.models.user_model import User


class   UserRepository:
    """
    Encapsula las operaciones de acceso a datos de usuarios.
    """

    def __init__(self, db: Session):
        # Recibimos la sesión que administra el ciclo de vida
        # de la conexión desde el router.
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        """
        Busca un usuario por su identificador.

        Devuelve un objeto User o None si no existe.
        """

        # Construimos la consulta SQL.
        statement = select(User).where(User.id == user_id)

        # Ejecutamos la consulta y obtenemos el primer resultado.
        return self.db.scalars(statement).first()

    def get_by_email(self, email: str) -> User | None:
        """
        Busca un usuario mediante su correo electrónico.
        """

        statement = select(User).where(User.email == email)

        return self.db.scalars(statement).first()

    def get_all(self, skip, limit) -> list[User]:
        """
        Recupera usuarios aplicando paginación.

        skip: cantidad de registros que se omiten.
        limit: cantidad máxima de registros devueltos.
        """

        statement = (
            select(User)
            .order_by(User.id)
            .offset(skip)
            .limit(limit)
        )

        return list(self.db.scalars(statement).all())

    def create(self, user: User) -> User:
        """
        Inserta un nuevo usuario en la base de datos.
        """

        # Agregamos el objeto a la sesión.
        self.db.add(user)

        # Confirmamos la transacción.
        self.db.commit()

        # Actualizamos el objeto con los valores persistidos,
        # como el ID generado por PostgreSQL.
        self.db.refresh(user)

        return user

    def update(self, user: User) -> User:
        """
        Confirma los cambios realizados sobre un usuario existente.
        """

        self.db.commit()
        self.db.refresh(user)

        return user

    def delete(self, user: User) -> None:
        """
        Elimina un usuario de la base de datos.
        """

        self.db.delete(user)
        self.db.commit()