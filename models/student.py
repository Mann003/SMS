from pydantic import BaseModel
from typing import Optional


class AddressBase(BaseModel):
    city: Optional[str]
    country: Optional[str]


class StudentBase(BaseModel):
    name: Optional[str]
    age: Optional[int]
    address: Optional[AddressBase]


class AddressCreate(AddressBase):
    city: str
    country: str


class StudentCreate(StudentBase):
    name: str
    age: int
    address: AddressCreate


class StudentUpdate(StudentBase):
    pass  # Optional fields are already handled in StudentBase


class AddressOut(AddressBase):
    city: str
    country: str


class StudentOut(StudentBase):
    name: str
    age: int
    address: AddressOut
