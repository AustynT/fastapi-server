from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.register import RegisterRequest, RegisterResponse
from app.schemas.token import TokenRequest, TokenResponse
from app.services.user_service import UserService
from app.services.token_service import TokenService
from app.db.database import get_db

router = APIRouter()

@router.post("/register", response_model=RegisterResponse, status_code=201)
def register_user(user_data: RegisterRequest, db: Session = Depends(get_db)):
    """
    Endpoint to register a new user.
    """
    user_service = UserService(db)  # Instantiate UserService
    return user_service.register_user(user_data)


@router.post("/login", response_model=RegisterResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint to authenticate a user.
    """
    user_service = UserService(db)  # Instantiate UserService
    return user_service.login_user(form_data.username, form_data.password)


@router.post("/logout")
def logout_user():
    """
    Logout a user. 
    Stateless logout.
    """
    # Logout functionality can be implemented using token blacklisting.
    return {"message": "User logged out successfully"}


@router.post("/refresh", response_model=TokenResponse)
def refresh_access_token(refresh_data: TokenRequest, db: Session = Depends(get_db)):
    """
    Endpoint to refresh an access token using a valid refresh token.
    """
    token_service = TokenService(db)  # Instantiate TokenService
    new_access_token = token_service.refresh_access_token(refresh_token_str=refresh_data.refresh_token)
    return TokenResponse(
        access_token=new_access_token,
        refresh_token=refresh_data.refresh_token,  # The same refresh token is returned
        token_type="bearer",
    )
