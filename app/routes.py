from fastapi import FastAPI, HTTPException, Path, Query, status
from typing import List, Optional
from bson import ObjectId
from app.database import database
from app.models import StudentCreate, StudentResponse, Address

app = FastAPI()
students_collection = database.get_students_collection()

@app.post("/students", status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentCreate):
    # Insert student record
    result = students_collection.insert_one(student.model_dump())
    
    # Return the ID of the newly created student
    return {"id": str(result.inserted_id)}

@app.get("/students", response_model=List[StudentResponse])
async def list_students(
    country: Optional[str] = Query(None), 
    age: Optional[int] = Query(None)
):
    # Build filter dynamically
    filter_query = {}
    if country:
        filter_query['address.country'] = country
    if age is not None:
        filter_query['age'] = {'$gte': age}

    # Fetch students
    students = list(students_collection.find(filter_query))
    
    # Convert to response model
    return [
        StudentResponse(
            id=str(student['_id']), 
            name=student['name'], 
            age=student['age'], 
            address=Address(**student['address'])
        ) for student in students
    ]

@app.get("/students/{id}", response_model=StudentResponse)
async def get_student(id: str = Path(...)):
    try:
        # Find student by ID
        student = students_collection.find_one({"_id": ObjectId(id)})
        
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        return StudentResponse(
            id=str(student['_id']), 
            name=student['name'], 
            age=student['age'], 
            address=Address(**student['address'])
        )
    except Exception:
        raise HTTPException(status_code=404, detail="Invalid student ID")

@app.patch("/students/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_student(id: str = Path(...), student_update: dict = {}):
    try:
        # Remove None values
        update_data = {k: v for k, v in student_update.items() if v is not None}
        
        # Update student
        result = students_collection.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        
        return None
    except Exception:
        raise HTTPException(status_code=404, detail="Invalid student ID")

@app.delete("/students/{id}", status_code=status.HTTP_200_OK)
async def delete_student(id: str = Path(...)):
    try:
        # Delete student
        result = students_collection.delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        
        return {}
    except Exception:
        raise HTTPException(status_code=404, detail="Invalid student ID")