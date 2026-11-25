from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user_model import User
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.schemas.user_schema import UserOut
from app.services.auth_service import AuthService


# get_current_user: Tu función de seguridad que extrae el token Bearer, verifica su
# firma JWT y busca al usuario dueño de ese token en PostgreSQL.
from app.core.dependencies import get_current_user

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
    db: Session = Depends(get_db)
):
    auth_service = AuthService(db)

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