from typing import Optional
from pydantic import BaseModel, Field, field_validator


class User(BaseModel):
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0, le=150)
    city: Optional[str] = None

    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return v.strip().title()
        return v
