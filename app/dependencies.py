from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .security import decode_access_token

def get_current_user(access_token: str | None = Cookie(default=None), db: Session = Depends(get_db)):
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login required")
    subject = decode_access_token(access_token)
    if not subject:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session")
    try:
        user = db.get(User, int(subject))
    except ValueError:
        user = None
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
