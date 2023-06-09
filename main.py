# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"
class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=20,
        example="Buenos Aires"
    )
    state: Optional[str] = Field(
        default=None,
        example="Boca"
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=20,
        example="Argentina"
    )
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "city": "Lima",
    #             "state": "SJL",
    #             "country": "Perú"
    #         }
    #     }
class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        le=100
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    class Config:
        schema_extra = {
            "example": {
                "first_name": "Jasumi Isaé",
                "last_name": "Palma Luna",
                "age": 13,
                "hair_color": "brown",
                "is_married": False
            }
        }

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
        description="This is the person name. It's between 1 and 10 characters.",
        example="Gabriela"
    ),
    age: int = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required.",
        example=27
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
        description="This is the person id. It's greater than 0.",
        example=1001
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
        description="This is the person id. It's greater than 0.",
        example=1
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return {person_id: results}

# Tipos de datos especiales
# Clásicos
# str
# int
# float
# bool
# Exóticos
# HttpUrl
# FilePath
# DirectoryPath
# EmailStr
# PaymentCardNumber
# IPvAnyAddress
# NegativeFloat
# PositiveFloat
# NegativeInt
# PositiveInt