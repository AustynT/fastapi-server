from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.models.token import Token
from app.schemas.user import RegisterRequest, RegisterResponse
from app.models.user import User
from app.db.database import get_db
from app.utils.security_utils import hash_password, verify_password
from app.core.config import config


router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user and return an access token.
    """
    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create a new user
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate and save the token
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = Token.create(
        user_id=new_user.id,
        expires_delta=expires_delta,
        payload={"sub": new_user.email},
        db=db,
    )

    # Return user data and token
    return RegisterResponse(
        id=new_user.id,
        email=new_user.email,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        created_at=new_user.created_at.isoformat(),
        updated_at=new_user.updated_at.isoformat(),
        access_token=token.token,
        token_type="bearer",
    )


@router.post("/login", response_model=RegisterResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login a user and return an access token.
    """
    # Validate user credentials
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    # Create and save the token in the database
    token = Token.create(
        user_id=user.id,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        payload={"sub": user.email},
        db=db,
    )

    # Return user data and token
    return RegisterResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        created_at=user.created_at.isoformat(),
        updated_at=user.updated_at.isoformat(),
        access_token=token.token,  # Use the token saved in the database
        token_type="bearer",
    )


@router.post("/logout")
def logout_user():
    """
    Logout a user. 
    Stateless logout.
    """
    # Logout functionality can be implemented using token blacklisting.
    return {"message": "User logged out successfully"}
