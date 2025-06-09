from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class ExpenseCreate(BaseModel):
    """Model for creating a new expense"""
    amount: float = Field(..., gt=0, description="Amount must be positive")
    description: str = Field(..., min_length=1, max_length=200, description="Expense description")
    paid_by: str = Field(..., min_length=1, max_length=50, description="Person who paid for the expense")
    
    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        if round(v, 2) != v:
            raise ValueError('Amount can have at most 2 decimal places')
        return round(v, 2)
    
    @validator('description')
    def validate_description(cls, v):
        if not v.strip():
            raise ValueError('Description cannot be empty or just whitespace')
        return v.strip()
    
    @validator('paid_by')
    def validate_paid_by(cls, v):
        if not v.strip():
            raise ValueError('Paid by cannot be empty or just whitespace')
        return v.strip().title()

class ExpenseUpdate(BaseModel):
    """Model for updating an existing expense"""
    amount: Optional[float] = Field(None, gt=0, description="Amount must be positive")
    description: Optional[str] = Field(None, min_length=1, max_length=200, description="Expense description")
    paid_by: Optional[str] = Field(None, min_length=1, max_length=50, description="Person who paid for the expense")
    
    @validator('amount')
    def validate_amount(cls, v):
        if v is not None:
            if v <= 0:
                raise ValueError('Amount must be positive')
            if round(v, 2) != v:
                raise ValueError('Amount can have at most 2 decimal places')
            return round(v, 2)
        return v
    
    @validator('description')
    def validate_description(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('Description cannot be empty or just whitespace')
            return v.strip()
        return v
    
    @validator('paid_by')
    def validate_paid_by(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('Paid by cannot be empty or just whitespace')
            return v.strip().title()
        return v

class ExpenseResponse(BaseModel):
    """Model for expense response"""
    id: int
    amount: float
    description: str
    paid_by: str
    created_at: datetime
    updated_at: datetime

class BalanceResponse(BaseModel):
    """Model for balance response"""
    person: str
    balance: float
    status: str  # "owes", "gets", "even"

class SettlementResponse(BaseModel):
    """Model for settlement response"""
    from_person: str
    to_person: str
    amount: float

class PersonResponse(BaseModel):
    """Model for person response"""
    name: str
    total_paid: float
    total_expenses: int
    balance: float
