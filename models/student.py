from pydantic import BaseModel
from typing import Optional, List


class AddressBase(BaseModel):
    city: Optional[str]
    country: Optional[str]


class StudentBase(BaseModel):
    name: Optional[str]
    age: Optional[int]
    address: Optional[AddressBase]


class StudentUpdate(StudentBase):
    pass  # Optional fields are already handled in StudentBase


class StudentList(BaseModel):
    name: str
    age: int


class StudentListResponse(BaseModel):
    data: List[StudentList]


class StudentPostResponse(BaseModel):
    id: str
