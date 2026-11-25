from fastapi import APIRouter, Depends

# get_auth_service inyecta el servicio de autenticación con su repositorio.
# get_current_user valida el token Bearer y devuelve el usuario autenticado.
from app.core.dependencies import get_auth_service, get_current_user
from app.models.user_model import User
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.schemas.user_schema import UserOut
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    access_token = auth_service.authenticate_user(
        email=login_data.email,
        password=login_data.password
    )

    return TokenResponse(
        access_token=access_token
    )


@router.get(
    "/me",
    response_model=UserOut
)
def read_current_user(
    current_user: User = Depends(get_current_user)
):
    return current_user