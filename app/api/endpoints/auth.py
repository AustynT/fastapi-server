from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import get_db
from app.utils.database_utils import add_and_commit
from app.models.user import User
from app.utils.security_utils import hash_password, verify_password, create_access_token
from app.core.config import config

router = APIRouter()

# Token expiration duration
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: dict, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == user_data.get("email")).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Hash the password and create a new user
    user_data["hashed_password"] = hash_password(user_data.pop("password"))
    new_user = User(**user_data)
    return add_and_commit(db, new_user)


@router.post("/login")
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
    
    # Create a JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout_user():
    """
    Logout a user. 
    Stateless logout.
    """
    # Logout functionality can be implemented using token blacklisting.
    return {"message": "User logged out successfully"}
