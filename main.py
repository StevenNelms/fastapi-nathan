from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os

app = FastAPI()

# Pull from environment variable set in Render
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL environment variable is not set!")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

@app.get("/")
def root():
    return {"message": "Nathan is live and listening 👂"}

@app.get("/people")
def read_people():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, first_name, last_name FROM people LIMIT 10"))
            rows = result.mappings().all()  # Convert rows to dictionaries
        return JSONResponse(content=rows)
    except SQLAlchemyError as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"❌ Database error: {str(e)}"}
        )
