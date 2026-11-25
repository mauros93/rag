# Depends: mecanismo de inyección de dependencias.
# status: proporciona constantes para los códigos HTTP.
# Path y Query: validan parámetros de ruta y de consulta.
from fastapi import APIRouter, Depends, Path, Query, status

# Dependencias compartidas de la capa HTTP.
from app.core.dependencies import get_user_service, require_admin

# User es el modelo ORM usado por las dependencias de autenticación.
from app.models.user_model import User

# ErrorResponse documenta la estructura de las respuestas de error.
from app.schemas.error_response import ErrorResponse

# UserIn define y valida los datos recibidos.
# UserOut define la estructura de la respuesta.
from app.schemas.user_schema import UserIn, UserOut, UserRoleUpdate, UserUpdate

# UserService contiene la lógica de negocio de los usuarios.
from app.services.user_service import UserService

# --------------------------------------------------
# 1. CONFIGURACIÓN DEL ROUTER
# --------------------------------------------------

# APIRouter permite organizar las rutas por módulos.
router = APIRouter(

    # Prefijo común para todos los endpoints de este router.
    # Por ejemplo: /users/
    prefix="/users",

    # Agrupa estos endpoints bajo la etiqueta Users
    # en la documentación automática de Swagger.
    tags=["Users"]
)




# response_model indica que la respuesta debe cumplir
# con la estructura definida en UserOut.
#
# status_code establece HTTP 201 Created cuando
# la operación se completa correctamente.
@router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
    response_description="El usuario ha sido creado exitosamente.",
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Datos de entrada inválidos o formato incorrecto."
        },
        409: {
            "model": ErrorResponse,
            "description": "El correo electrónico o nombre de usuario ya existe."
        }
    }
)
def create_user(

    # FastAPI interpreta este parámetro como el cuerpo
    # JSON de la solicitud y lo valida mediante UserIn.
    user_data: UserIn,

    # FastAPI inyecta el servicio con su repositorio ya configurado.
    user_service: UserService = Depends(get_user_service)
):

    """
    Crea un nuevo usuario en el sistema con la información proporcionada.

    - **name**: Nombre completo del usuario.
    - **email**: Debe ser un correo electrónico válido y único.
    - **password**: Mínimo 8 caracteres, al menos un número y un símbolo.
    """

    # Delegamos la operación al servicio, que aplica las reglas
    # de negocio y usa el repositorio para guardar el usuario.
    return user_service.create_user(user_data)


# --------------------------------------------------
# 2. OBTENER TODOS LOS USUARIOS 
# --------------------------------------------------

@router.get(
    "/",
    response_model=list[UserOut],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    response_description="Lista con todos los usuarios registrados."
)
def get_users(
    skip: int = Query(
        default=0,
        ge=0,
        description="Cantidad de usuarios que se deben omitir."
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
        description="Cantidad máxima de usuarios por página."
    ),
    current_user: User = Depends(require_admin),
    user_service: UserService = Depends(get_user_service)
):
    """
    Recupera usuarios mediante paginación.

    El límite máximo permitido es de 50 usuarios por solicitud.
    """

    return user_service.get_all_users(
        skip=skip,
        limit=limit
)


@router.patch(
    "/{user_id}/role",
    response_model=UserOut
)
def update_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    current_user: User = Depends(require_admin),
    user_service: UserService = Depends(get_user_service)
):
    return user_service.update_user_role(
        user_id=user_id,
        new_role=role_data.role
    )


@router.get(
    "/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por ID",
    response_description="Detalles completos del usuario solicitado.",
    responses={
        404: {
            "model": ErrorResponse,
            "description": "El usuario con el ID especificado no fue encontrado."
        }
    }
)   
def get_user(
    user_id: int = Path(
        ...,
        title="ID del Usuario",
        description="Identificador numérico único del usuario en la base de datos.",
        example=1,
        gt=0
    ),
    user_service: UserService = Depends(get_user_service)
):
    """
    Recupera la información detallada de un usuario según su **ID numérico**.
    """
    return user_service.get_user_by_id(user_id)



@router.patch(
    "/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Actualizar parcialmente un usuario",
    responses={
        404: {"model": ErrorResponse, "description": "Usuario no encontrado"},
        409: {"model": ErrorResponse, "description": "El correo electrónico ya existe"},
        422: {"model": ErrorResponse, "description": "Datos de actualización inválidos"}
    }
)
def update_user(
    user_data: UserUpdate,
    user_id: int = Path(..., gt=0),
    user_service: UserService = Depends(get_user_service)
):
    return user_service.update_user(user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un usuario",
    responses={
        404: {"model": ErrorResponse, "description": "Usuario no encontrado"}
    }
)
def delete_user(
    user_id: int = Path(..., gt=0),
    user_service: UserService = Depends(get_user_service)
):
    user_service.delete_user(user_id)



