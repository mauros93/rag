from fastapi import HTTPException, status

# Session sirve para gestionar la conexión con la base de datos
from sqlalchemy.orm import Session

# select se usa para hacer las consultas sql
from sqlalchemy import select

from app.models.user_model import User
from app.core.security import (
    verify_password,
    create_access_token
)



class AuthService:

    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(
        self,
        email: str,
        password: str
    ) -> str:

        statement = select(User).where(User.email == email)

        user = self.db.scalars(statement).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access_token = create_access_token(
            subject=user.id
        )

        return access_token

    