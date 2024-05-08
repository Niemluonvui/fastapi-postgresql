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
        if table_search == None:
            return("Khong co table!")
        with db.connection() as conn:
            if key == None:
                sele = select(table_search)
                result = conn.execute(sele)
            elif key.isnumeric():
                sele = select(table_search).where(table_search.id == int(key))
                result = conn.execute(sele)
            else:
                check = db.query(table_search).filter(table_search.name == key).scalar()
                if check != None:
                    sele = select(table_search).where(table_search.name == key)
                    print(sele)
                else:
                    sele = select(table_search)
                result = conn.execute(sele)
        for row in result:
            print(row)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/{table}/delete/{key}")
async def delete_table(db: db_dependancy, table: str, key: str = None):
    try:
        table_search = tables_dict.get(table)
        if table_search == None:
            return("Khong co table!")
        with db.connection() as conn:
            if key.isnumeric():
                dele = delete(table_search).where(table_search.id==int(key))
            elif key != None:
                dele = delete(table_search).where(table_search.name==key)
            else:
                return ("missing id or text")
            
            conn.execute(dele)
            conn.commit()
            return ("done!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/{table}/update/{id}/{content}")
async def update_table(db: db_dependancy, table: str, id: int, content: str):    
    try:
        table_search = tables_dict.get(table)
        if table_search == None:
            return("Khong co table!")
        with db.connection() as conn:
            if id:
                if content:
                    upd = update(table_search).where(table_search.id == id).values( name = content)
                    conn.execute(upd)
                    conn.commit()
                else:
                    return("missing content!")
            else:
                return("missing id!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/{table}/insert/{id}/{content}")
async def add_category(db: db_dependancy, table: str, id: int, content: str):
    try:
        table_search = tables_dict.get(table)
        if table_search == None:
            return("Khong co table!")
        with db.connection() as conn:
            if id:
                if content:
                    ins = insert(table_search).values(id = id, name = content)
                    conn.execute(ins)
                    conn.commit()
                else:
                    return("missing content!")
            else:
                return("missing id!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")