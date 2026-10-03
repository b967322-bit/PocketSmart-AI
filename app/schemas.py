from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=8, max_length=128)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class HomeRequest(BaseModel):
    budget: float = Field(gt=0)
    city: str = Field(default="Chennai", min_length=2, max_length=100)
    rooms: list[str] = Field(default_factory=list)
    style: str = Field(default="Modern")
    items: dict[str, int] = Field(default_factory=dict)

class PartyRequest(BaseModel):
    budget: float = Field(gt=0)
    city: str = Field(default="Chennai", min_length=2, max_length=100)
    guests: int = Field(gt=0, le=10000)
    event_type: str = Field(min_length=2, max_length=80)
    venue: str = Field(default="Flexible", max_length=120)
    preferences: str = Field(default="", max_length=1000)

class JewelryRequest(BaseModel):
    budget: float = Field(gt=0)
    occasion: str = Field(min_length=2, max_length=100)
    style: str = Field(default="Elegant", max_length=100)
    outfit_notes: str = Field(default="", max_length=1000)
