from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated
from models import tables_dict
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import insert, delete, update, select

app = FastAPI()

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

@app.get("/{table}/query/{key}")
async def query_table(db: db_dependancy, table: str, key: str = None):
    try:
        table_search = tables_dict.get(table)
        with db.connection() as conn:
            if key == None:
                sele = select(table)
                result = conn.execute(sele)
            elif key.isnumeric():
                sele = select(table_search).where(table_search.id == int(key))
                result = conn.execute(sele)
                # sele = text(f"SELECT * FROM {table} WHERE {table}.category_id = :value")
                # result = conn.execute(sele, {"value": key})
            else:
                sele = select(table_search)
                result = conn.execute(sele)
        for row in result:
            print(row)
    except:
        raise HTTPException()

@app.post("/{table}/delete/{key}")
async def delete_table(db: db_dependancy, table: str, key: str = None):
    try:
        with db.connection() as conn:
            table_search = tables_dict.get(table)
            if key.isnumeric():
                dele = delete(table_search).where(table_search.id==int(key))
            elif key != None:
                dele = delete(table_search).where(table_search.name==key)
            else:
                return ("missing id or text")
            
            conn.execute(dele)
            
            return ("done!")
    except:
        raise HTTPException()

@app.post("/{table}/update/{id}/{content}")
async def update_table(db: db_dependancy, table: str, id: int, content: str):    
    try:
        with db.connection() as conn:
            table_search = tables_dict.get(table)
            if id:
                upd = update(table_search).values({"name": content}).where(table_search.id == id)
                engine.execute(upd).fetchall()
            else:
                return("missing id!")
    except:
        raise HTTPException()

@app.put("/{table}/insert/{id}/{content}")
async def query_category(db: db_dependancy, table: str, id: int, content: str):
    try:
        with db.connection() as conn:
            table_search = tables_dict.get(table)
            if id:
                upd = insert(table_search).values({"id": id, "name": content})
                engine.execute(upd).fetchall()
            else:
                return("missing id!")
    except:
        raise HTTPException()

@app.post("/{table}/insert/{id}/{content}")
async def add_category(db: db_dependancy, table: str, id: int, content: str):
    db_category = category(id= id, name=name)
    db.add(db_category)
    db.commit()
    return db_category

