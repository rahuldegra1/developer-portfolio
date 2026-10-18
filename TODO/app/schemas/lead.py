from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class LeadBase(BaseModel):
    full_name: str
    email: str
    budget_inr: int = Field(gt=0, description="Budget in INR, must be positive")
    phone: str

    @field_validator("full_name", mode="before")
    @classmethod
    def clean_name(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip().title()
        return value

    @field_validator("email", mode="before")
    @classmethod
    def clean_and_validate_email(cls, value: str) -> str:
        if isinstance(value, str):
            cleaned = value.strip().lower()
            if "@" not in cleaned:
                raise ValueError("Invalid email: missing '@' symbol")
            return cleaned
        return value

    @field_validator("budget_inr", mode="before")
    @classmethod
    def clean_budget(cls, value):
        if isinstance(value, str):
            cleaned = value.replace("₹", "").replace(",", "").strip()
            return int(cleaned)
        return value

    @field_validator("phone", mode="before")
    @classmethod
    def clean_phone(cls, value: str) -> str:
        if isinstance(value, str):
            cleaned = value.replace("-", "").replace(" ", "").replace("+", "").strip()
            if not cleaned.isdigit() or len(cleaned) != 10:
                raise ValueError("Phone number must contain exactly 10 digits")
            return cleaned
        return value


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    budget_inr: Optional[int] = Field(default=None, gt=0)
    phone: Optional[str] = None

    @field_validator("full_name", mode="before")
    @classmethod
    def clean_name(cls, value):
        if isinstance(value, str):
            return value.strip().title()
        return value

    @field_validator("email", mode="before")
    @classmethod
    def clean_email(cls, value):
        if isinstance(value, str):
            cleaned = value.strip().lower()
            if "@" not in cleaned:
                raise ValueError("Invalid email: missing '@' symbol")
            return cleaned
        return value

    @field_validator("budget_inr", mode="before")
    @classmethod
    def clean_budget(cls, value):
        if isinstance(value, str):
            cleaned = value.replace("₹", "").replace(",", "").strip()
            return int(cleaned)
        return value

    @field_validator("phone", mode="before")
    @classmethod
    def clean_phone(cls, value):
        if isinstance(value, str):
            cleaned = value.replace("-", "").replace(" ", "").replace("+", "").strip()
            if not cleaned.isdigit() or len(cleaned) != 10:
                raise ValueError("Phone number must contain exactly 10 digits")
            return cleaned
        return value


class LeadResponse(LeadBase):
    id: int

    class Config:
        from_attributes = True


class PaginatedLeadResponse(BaseModel):
    total_count: int
    skip: int
    limit: int
    data: List[LeadResponse]