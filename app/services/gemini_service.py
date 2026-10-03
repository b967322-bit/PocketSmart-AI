import json
import re
from typing import Any
from .catalog import enrich_recommendations
from .prompts import home_prompt, party_prompt, jewelry_prompt
from ..config import get_settings

def _extract_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        value = json.loads(text)
        return value if isinstance(value, dict) else None
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            return None
        try:
            value = json.loads(match.group(0))
            return value if isinstance(value, dict) else None
        except json.JSONDecodeError:
            return None

def _fallback(planner, data):
    budget = float(data["budget"])
    if planner == "home":
        allocations = [("Furniture", .35), ("Lighting", .15), ("Decor", .20), ("Storage", .20), ("Buffer", .10)]
        names = [("Compact modern sofa","Furniture","Amazon"),("Warm LED ceiling light","Lighting","IKEA"),
                 ("Minimal wall decor set","Decor","Flipkart"),("Modular storage unit","Storage","IKEA")]
    elif planner == "party":
        allocations = [("Food/Catering", .45), ("Venue", .25), ("Decoration", .15), ("Entertainment", .10), ("Buffer", .05)]
        names = [("Catering package","Food/Catering","Zomato"),("Budget event venue","Venue","OYO"),
                 ("Party decoration kit","Decoration","Amazon"),("Simple entertainment package","Entertainment","Swiggy")]
    else:
        allocations = [("Necklace/Earrings", .55), ("Bangles", .20), ("Complementary piece", .15), ("Buffer", .10)]
        names = [("Elegant necklace and earring set","Necklace/Earrings","Amazon"),
                 ("Classic bangles","Bangles","Flipkart"),("Matching accessory","Complementary piece","Amazon")]
    result = {
        "summary": f"Fallback {planner} plan generated because Gemini was unavailable.",
        "budget_allocation": [{"category": c, "amount": round(budget*p, 2)} for c,p in allocations],
        "recommendations": [],
        "tips": ["Keep a small buffer for price changes.", "Verify product/service details on the linked platform."],
        "source": "fallback"
    }
    for i, (name, category, platform) in enumerate(names):
        estimate = round(budget * allocations[min(i, len(allocations)-1)][1] * .75, 2)
        result["recommendations"].append({
            "name": name, "category": category, "estimated_price": estimate,
            "platform": platform, "reason": "Local fallback estimate; verify current price before purchase."
        })
    return enrich_recommendations(result)

class GeminiService:
    def __init__(self):
        settings = get_settings()
        self.api_key = settings.gemini_api_key
        self.model = settings.gemini_model
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except Exception:
                self.client = None

    def generate(self, planner, data, image_bytes=None, mime_type=None):
        if not self.client:
            return _fallback(planner, data)
        prompt = home_prompt(data) if planner == "home" else party_prompt(data) if planner == "party" else jewelry_prompt(data, bool(image_bytes))
        contents: list[Any] = [prompt]
        if image_bytes:
            from google.genai import types
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type or "image/jpeg"))
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config={"response_mime_type": "application/json"},
            )
            result = _extract_json(response.text or "")
            if not result:
                return _fallback(planner, data)
            result.setdefault("source", "gemini")
            return enrich_recommendations(result)
        except Exception:
            return _fallback(planner, data)
