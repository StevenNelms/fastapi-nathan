from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from pydantic import BaseModel

app = FastAPI()

# Database config
DATABASE_URL = "postgresql://postgres:FoogimaFoogima123!@localhost:5432/productive_resource_db"
engine = create_engine(DATABASE_URL)

# Response schema
class Person(BaseModel):
    id: str
    first_name: str | None = None
    last_name: str | None = None

@app.get("/people", response_model=List[Person])
def get_people():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT id, first_name, last_name
                FROM people
                ORDER BY id
                LIMIT 10
            """))

            people = []
            for row in result:
                person = {
                    "id": str(row[0]),
                    "first_name": row[1] if row[1] else None,
                    "last_name": row[2] if row[2] else None
                }
                people.append(person)

            return people

    except SQLAlchemyError as e:
        print("❌ Database error:", e)
        return []
