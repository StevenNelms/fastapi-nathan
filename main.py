from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# --- App Setup ---
app = FastAPI()

# --- Database Connection ---
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL environment variable is not set!")

engine = create_engine(DATABASE_URL)

# --- Routes ---
@app.get("/")
def root():
    return {"message": "✅ Nathan API is live and connected!"}

@app.get("/people")
def read_people():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, first_name, last_name FROM people LIMIT 10"))
            people = [dict(row) for row in result.mappings().all()]  # ✅ Fixed serialization
        return JSONResponse(content=people)
    except SQLAlchemyError as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"❌ Database error: {str(e)}"}
        )
