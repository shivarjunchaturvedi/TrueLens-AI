from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import UserRegister, UserLogin, Token, UserOut
from app.services.auth_service import register_user, authenticate_user
from app.security.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    """Create a new user account. Passwords are bcrypt-hashed before storage."""
    user = register_user(db, payload)
    return user


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """Authenticate and return a JWT access token."""
    user = authenticate_user(db, payload.username, payload.password)
    token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=token, user=UserOut.model_validate(user))
