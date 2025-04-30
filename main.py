from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os

# ── App Setup ──
app = FastAPI(title="Nathan's API")

# ── Database Connection ──
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL environment variable is not set!")

engine = create_engine(DATABASE_URL)

# ── Valid views ──
VALID_VIEWS = {
    "assignment_summary",
    "staffing_candidates",
    "burn_entries",
    "burn_cumulative",
    "deals_summary",
    "certified_people",
    "people_profile",
    "time_entries_flat",
    "utilization_summary",
    "budgets_summary",
    "gantt_assignments",
    "service_burn_entries",
    "pending_assignments_summary"
}

# ── Routes ──

@app.get("/")
def root():
    return {"message": "✅ Nathan API is live and connected!"}

@app.get("/people")
def read_people():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, first_name, last_name FROM people LIMIT 10"))
            people = [dict(row) for row in result.mappings().all()]
        return JSONResponse(content=people)
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"❌ Database error: {str(e)}"})

@app.get("/views/{view_name}")
def read_view(view_name: str):
    if view_name not in VALID_VIEWS:
        return JSONResponse(status_code=400, content={"error": "❌ Invalid view name"})

    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {view_name}"))
            rows = [dict(row) for row in result.mappings().all()]
        return {"rows": rows}
    except SQLAlchemyError as e:
        return JSONResponse(status_code=500, content={"error": f"❌ Database error: {str(e)}"})
