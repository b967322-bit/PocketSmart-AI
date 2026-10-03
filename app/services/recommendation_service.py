import json
from ..models import RecommendationHistory
from .gemini_service import GeminiService

class RecommendationService:
    def __init__(self):
        self.ai = GeminiService()

    def create(self, db, user, planner, payload, image_bytes=None, mime_type=None):
        result = self.ai.generate(planner, payload, image_bytes, mime_type)
        row = RecommendationHistory(
            user_id=user.id,
            planner=planner,
            budget=float(payload["budget"]),
            request_json=json.dumps(payload, ensure_ascii=False),
            result_json=json.dumps(result, ensure_ascii=False),
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return row, result

    @staticmethod
    def parse(row):
        return {
            "id": row.id, "planner": row.planner, "budget": row.budget,
            "created_at": row.created_at.isoformat(),
            "request": json.loads(row.request_json),
            "result": json.loads(row.result_json),
        }
