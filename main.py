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

@app.get("/category/delete/")
async def delete_category(db: db_dependancy, id: int = None, name: str = None):
    if id:
        dele = delete(models.category).where(models.category.category_id==id)
    elif name:
        dele = delete(models.category).where(models.category.name==name)
    else:
        return ("missing id or text")
    
    engine.execute(dele)
    
    return ("done!")

@app.get("/category/update/")
async def update_category(db: db_dependancy, id: int = None, name: str = None):
    if id:
        db_category = db.query(models.category).filter_by(category_id = id).all()
        upd = update(models.category).values({"name": name}).where(models.category.category_id == id)
        engine.execute(upd)
        return ("done!")
    else:
        return ("missing id!")

@app.get("/category/query/")
async def query_category(db: db_dependancy, id: int = None, name: str = None):
    if id:
        db_category = db.query(models.category).filter_by(category_id = id).all()
    elif name == 'all':
        db_category = db.query(models.category).all()
    elif name:
        db_category = db.query(models.category).filter_by(name = name).all()
    else:
        return ("not query any")
    
    for result in db_category:
        print(result.name)
        print(str(result.category_id) + "\n")

@app.get("/category/")
async def add_category(db: db_dependancy, id: int, name: str = None):
    db_category = models.Category(category_id= id, name=name)
    db.add(db_category)
    db.commit()
    return db_category

