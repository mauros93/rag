# String define columnas de texto en PostgreSQL.
from sqlalchemy import String

from enum import Enum

# Mapped y mapped_column permiten definir columnas
# utilizando el sistema de tipado de SQLAlchemy 2.0.
from sqlalchemy.orm import Mapped, mapped_column

# Importamos nuestra clase declarativa Base.
from app.db.base import Base


# Define los roles disponibles en la aplicación.
#
# Al utilizar str y Enum, cada valor también se comporta
# como una cadena de texto.
class UserRole(str, Enum):

    # Usuario con permisos administrativos.
    ADMIN = "admin"

    # Usuario estándar de la aplicación.
    USER = "user"


# Esta clase representa la tabla users.
class User(Base):

    

    # Nombre de la tabla en PostgreSQL.
    __tablename__ = "users"

    # Identificador único del usuario.
    #
    # primary_key=True indica que será la clave primaria.
    # SQLAlchemy configura el autoincremento correspondiente.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Nombre del usuario.
    #
    # String(100) establece una longitud máxima de 100 caracteres.
    # nullable=False impide almacenar valores nulos.
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # Correo electrónico del usuario.
    #
    # unique=True impide que dos usuarios tengan
    # el mismo correo electrónico.
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    # Hash de la contraseña del usuario (Requerido por UserService).
    # String(255) es suficiente para almacenar hashes generados por bcrypt o argon2.
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )


    # Rol asignado al usuario.
    #
    # Por defecto, los nuevos usuarios tendrán el rol USER.
    role: Mapped[UserRole] = mapped_column(
        String(20),
        default=UserRole.USER,
        nullable=False
    ) 

    
