# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models
class Location(BaseModel):
    city: str
    state: Optional[str]
    country: str
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {"Hello": "World"}

# Request and Response Body
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validations: Query Parameters
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=10,
        title="Person Name",
        description="This is the person name. It's between 1 and 10 characters."
    ),
    age: int = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required."
    )
):
    return {name: age}

# Validations: Path Parameters
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title="Person Id",
        description="This is the person id. It's greater than 0."
    )
):
    return {person_id: "It's exists!"}

# Validations: Request Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title="Person Id",
        description="This is the person id. It's greater than 0."
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results