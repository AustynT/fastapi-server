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
    return UserService.register_user(user_data, db)


@router.post("/login", response_model=RegisterResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint to authenticate a user.
    """
    return UserService.login_user(form_data.username, form_data.password, db)


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
    try:
        # Use the TokenService to refresh the access token
        new_access_token = TokenService.refresh_access_token(
            refresh_token_str=refresh_data.refresh_token,
            db=db
        )
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=refresh_data.refresh_token,  # The same refresh token is returned
            token_type="bearer",
        )
    except HTTPException as e:
        raise e
