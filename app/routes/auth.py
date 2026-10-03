from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user
from ..models import User, RecommendationHistory
from ..schemas import LoginRequest, RegisterRequest
from ..security import create_access_token, hash_password, verify_password

router = APIRouter()

@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.scalar(select(User).where(User.email == payload.email.lower()))
    if existing:
        raise HTTPException(409, "Email is already registered")
    user = User(email=payload.email.lower(), full_name=payload.full_name.strip(), password_hash=hash_password(payload.password))
    db.add(user); db.commit(); db.refresh(user)
    return {"message": "Registration successful", "user_id": user.id}

def _login(response, payload, db):
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")
    token = create_access_token(str(user.id))
    response.set_cookie("access_token", token, httponly=True, samesite="lax", max_age=7200)
    return {"message": "Login successful", "user": {"id": user.id, "email": user.email, "full_name": user.full_name}}

@router.post("/login")
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    return _login(response, payload, db)

@router.post("/token")
def token(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    return _login(response, payload, db)

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}

@router.get("/session-info")
def session_info(user: User = Depends(get_current_user)):
    return {"logged_in": True, "user_id": user.id, "email": user.email, "full_name": user.full_name}

@router.get("/session-data")
def session_data(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from ..services.recommendation_service import RecommendationService
    rows = db.scalars(
        select(RecommendationHistory)
        .where(RecommendationHistory.user_id == user.id)
        .order_by(RecommendationHistory.created_at.desc()).limit(5)
    ).all()
    return {"user": {"id": user.id, "email": user.email, "full_name": user.full_name},
            "recent": [RecommendationService.parse(x) for x in rows]}
