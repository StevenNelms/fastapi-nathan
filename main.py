from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from typing import List
import os

app = FastAPI(title="Nathan's FastAPI")

# Update this connection string if your database config changes
DATABASE_URL = "postgresql://postgres:FoogimaFoogima123!@localhost:5432/productive_resource_db"
engine = create_engine(DATABASE_URL)


# Define the response model for a Person
class Person(BaseModel):
    id: str
    first_name: str
    last_name: str | None = None


@app.get("/people", response_model=List[Person])
def get_people():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT id, first_name, last_name
                FROM people
                ORDER BY first_name
                LIMIT 10
            """))

            people = [
                {"id": str(row[0]), "first_name": row[1], "last_name": row[2]}
                for row in result
            ]

        return people

    except SQLAlchemyError as e:
        print("❌ Database error:", e)
        return []
