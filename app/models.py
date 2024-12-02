from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class Address(BaseModel):
    city: str
    country: str

class StudentCreate(BaseModel):
    name: str
    age: int = Field(..., ge=0)
    address: Address

class StudentResponse(StudentCreate):
    id: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }