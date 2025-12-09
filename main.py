from fastapi import FastAPI, Request, Form, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from sqlalchemy import create_engine, text, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import io

app = FastAPI(title="Naija Schools DB")
templates = Jinja2Templates(directory="templates")

engine = create_engine("sqlite:///schools.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()

class School(Base):
    __tablename__ = "schools"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    lga = Column(String)
    state = Column(String)
    type = Column(String)  # Primary, Secondary, Tertiary
    ownership = Column(String)  # Public, Private, Mission

Base.metadata.create_all(engine)

@app.get("/", response_class=HTMLResponse)
@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request, q: str = ""):
    session = Session()
    query = "SELECT * FROM schools"
    if q:
        query += f" WHERE name LIKE '%{q}%' OR lga LIKE '%{q}%' OR state LIKE '%{q}%'"
    df = pd.read_sql(query, engine)
    session.close()
    return templates.TemplateResponse("admin.html", {"request": request, "schools": df.to_dict("records"), "q": q})

@app.post("/add")
def add(name: str = Form(), lga: str = Form(), state: str = Form(), type: str = Form(), ownership: str = Form()):
    session = Session()
    session.execute(text("INSERT INTO schools (name,lga,state,type,ownership) VALUES (:n,:l,:s,:t,:o)"),
                    {"n":name,"l":lga,"s":state,"t":type,"o":ownership})
    session.commit()
    session.close()
    return {"status": "added"}

@app.get("/export")
def export(q: str = ""):
    :
    session = Session()
    query = "SELECT * FROM schools"
    if q:
        query += f" WHERE name LIKE '%{q}%' OR lga LIKE '%{q}%'"
    df = pd.read_sql(query, engine)
    session.close()
    
    output = io.BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    return StreamingResponse(output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            headers={"Content-Disposition": "attachment; filename=naija_schools.xlsx"})
