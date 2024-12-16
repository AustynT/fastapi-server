from app.models.user import User
from app.schemas.register import RegisterRequest, RegisterResponse
from app.schemas.token import TokenResponse
from app.utils.security_utils import hash_password, verify_password
from app.services.token_service import TokenService
from app.services.base_service import BaseService
from fastapi import HTTPException, status


class UserService(BaseService):
    def __init__(self, db):
        super().__init__(db)
        self.token_service = TokenService(db)

    def register_user(self, user_data: RegisterRequest) -> RegisterResponse:
        """
        Register a new user and return their details along with an access token.
        """
        existing_user = self._database.db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed_password = hash_password(user_data.password)
        new_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )

        new_user = self._database.add_and_commit(new_user)

        token = self.token_service.create_token(
            user_id=new_user.id,
            payload={"sub": new_user.email},
        )

        return RegisterResponse(
            id=new_user.id,
            email=new_user.email,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            created_at=new_user.created_at.isoformat(),
            updated_at=new_user.updated_at.isoformat(),
            token=TokenResponse(
                access_token=token.token,
                refresh_token=token.refresh_token,
                token_type="bearer",
            ),
        )

    def login_user(self, email: str, password: str) -> RegisterResponse:
        """
        Authenticate a user and return their details along with an access token.
        """
        user = self._database.db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        token = self.token_service.create_token(
            user_id=user.id,
            payload={"sub": user.email},
        )

        return RegisterResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat(),
            token=TokenResponse(
                access_token=token.token,
                refresh_token=token.refresh_token,
                token_type="bearer",
            ),
        )
