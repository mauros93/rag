
# BaseModel: clase base de Pydantic para crear schemas.
# ConfigDict: permite configurar el comportamiento de los schemas.
# EmailStr: valida que el correo tenga un formato válido.
from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.user_model import UserRole




# Contiene los campos compartidos entre los diferentes
# schemas de usuario.
#
# Utilizamos herencia para evitar repetir las mismas
# definiciones en UserCreate y UserOut.
class UserBase(BaseModel):


    name: str

    # Correo electrónico.
    # EmailStr valida que tenga un formato de email válido.
    email: EmailStr



# Define los datos que el cliente debe enviar
# cuando solicita registrar un nuevo usuario.
class UserIn(UserBase):
    password: str

    # Asi evitamos que envien campos extras
    model_config = ConfigDict(extra="forbid")



# Define los datos que nuestra API puede devolver
class UserOut(UserBase):

    # Identificador único generado por PostgreSQL.
    id: int

    # define el role del usuario
    role: UserRole

    # Configuración de Pydantic.
    #
    # from_attributes=True permite construir este schema
    # directamente desde un objeto ORM de SQLAlchemy.
    #
    # Por ejemplo:
    # user_out = UserOut.model_validate(user_model)
    #
    # Sin esta configuración, Pydantic esperaría
    # normalmente un diccionario u otro objeto compatible.  
    model_config = ConfigDict(from_attributes=True)



class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class UserRoleUpdate(BaseModel):
    role: UserRole

    model_config = ConfigDict(extra="forbid")