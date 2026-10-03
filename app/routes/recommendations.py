from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user
from ..models import RecommendationHistory, User
from ..schemas import HomeRequest, PartyRequest
from ..services.recommendation_service import RecommendationService

router = APIRouter()
service = RecommendationService()

@router.post("/generate-home")
def generate_home(payload: HomeRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    row, result = service.create(db, user, "home", payload.model_dump())
    return {"id": row.id, **result}

@router.post("/generate-party")
def generate_party(payload: PartyRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    row, result = service.create(db, user, "party", payload.model_dump())
    return {"id": row.id, **result}

@router.post("/generate-jewelry")
async def generate_jewelry(
    budget: float = Form(...), occasion: str = Form(...), style: str = Form("Elegant"),
    outfit_notes: str = Form(""), outfit_image: UploadFile | None = File(default=None),
    db: Session = Depends(get_db), user: User = Depends(get_current_user),
):
    image_bytes = await outfit_image.read() if outfit_image else None
    mime_type = outfit_image.content_type if outfit_image else None
    payload = {"budget": budget, "occasion": occasion, "style": style, "outfit_notes": outfit_notes}
    row, result = service.create(db, user, "jewelry", payload, image_bytes, mime_type)
    return {"id": row.id, **result}

@router.get("/recommendations-details/{recommendation_id}")
def recommendation_details(recommendation_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    row = db.scalar(select(RecommendationHistory).where(
        RecommendationHistory.id == recommendation_id,
        RecommendationHistory.user_id == user.id,
    ))
    if not row:
        raise HTTPException(404, "Recommendation not found")
    return service.parse(row)

@router.get("/history")
def history(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    rows = db.scalars(select(RecommendationHistory)
        .where(RecommendationHistory.user_id == user.id)
        .order_by(RecommendationHistory.created_at.desc())).all()
    return {"items": [service.parse(x) for x in rows]}
