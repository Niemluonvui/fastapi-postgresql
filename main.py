from fastapi import FastAPI, HTTPException, Depends
from typing import List, Annotated
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import insert, delete, update, select

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
    
class Items(BaseModel):
    id: int
    title: str
    
class Users(BaseModel):
    id: int
    email: str
    items: List[Items]
    
class Cate(BaseModel):
    category_id: int
    name: str
    
class country(BaseModel):
    country_id: int
    country_name: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependancy = Annotated[Session, Depends(get_db)]

@app.get("/category/query/{id}")
async def query_category_id(db: db_dependancy, id: int):
    db_category = db.query(models.Category).filter_by(category_id = id).all()
    print(db_category[0].category_id)
    print(db_category[0].name)
    return ( db_category[0].name )

@app.get("/category/query/{name}")
async def query_category_id(db: db_dependancy, name: str):
    db_category = db.query(models.Category).filter_by(name = name).all()
    print(db_category[0].category_id)
    print(db_category[0].name)
    return ( db_category[0].category_id )

@app.get("/category/")
async def add_category(db: db_dependancy, id: int, name: str = None):
    db_category = models.Category(category_id= id, name=name)
    db.add(db_category)
    db.commit()
    return db_category

