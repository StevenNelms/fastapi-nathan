from fastapi import FastAPI
from sqlalchemy import create_engine, text
import os

app = FastAPI()

# Database connection
DATABASE_URL = "postgresql://postgres:FoogimaFoogima123!@localhost:5432/productive_resource_db"
engine = create_engine(DATABASE_URL)

@app.get("/")
def root():
    return {"message": "Nathan is online!"}

@app.get("/people")
def read_people():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, first_name, last_name FROM people LIMIT 10"))
        return result.mappings().all()