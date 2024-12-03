from typing import Optional, List
from bson.errors import InvalidId
from fastapi import APIRouter, Query, HTTPException, Path
from models.student import StudentCreate, StudentOut, StudentUpdate
from config.database import db
from bson import ObjectId

studentRouter = APIRouter()

students_collection = db["students"]


@studentRouter.post("/students", response_model=StudentOut, status_code=201)
async def create_student(student: StudentCreate):
    # Convert Pydantic model to dictionary
    student_dict = student.dict()
    result = students_collection.insert_one(student_dict)
    return {"id": str(result.inserted_id)}


@studentRouter.get("/students", response_model=List[StudentOut], status_code=200)
async def list_students(
        country: Optional[str] = Query(None, description="Filter by country"),
        age: Optional[int] = Query(None, description="Filter by minimum age"),
):
    query = {}
    if country:
        query["address.country"] = country
    if age is not None:
        query["age"] = {"$gte": age}

    # Fetch data synchronously and convert to a list
    students_cursor = students_collection.find(query, {"_id": 0, "name": 1, "age": 1})
    students = list(students_cursor)
    return students


@studentRouter.get("/students/{id}", response_model=StudentOut, status_code=200)
async def fetch_student(id: str = Path(..., description="The ID of the student previously created")):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format")

        student = students_collection.find_one({"_id": ObjectId(id)})
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Transform MongoDB document to the response format
        student["id"] = str(student["_id"])
        del student["_id"]
        return student

    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")


@studentRouter.patch("/students/{id}", response_model=None, status_code=204)
async def update_student(
        id: str = Path(..., description="The ID of the student to update"),
        student: StudentUpdate = None
):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format")

        # Convert the incoming data to a dictionary and remove None values
        update_data = {k: v for k, v in student.dict(exclude_unset=True).items() if v is not None}

        if "address" in update_data:
            update_data["address"] = {k: v for k, v in update_data["address"].items() if v is not None}

        # Ensure there's data to update
        if not update_data:
            raise HTTPException(status_code=400, detail="No data provided for update")

        # Perform the update operation
        result = students_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")

        return {"message": "Student updated successfully"}

    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid ID format")


@studentRouter.delete("/students/{id}", response_model=dict, status_code=200)
async def delete_student(
        id: str = Path(..., description="The ID of the student to delete")
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    # Attempt to delete the student
    result = students_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student deleted successfully"}
