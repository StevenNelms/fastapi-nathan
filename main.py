import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# ── App Setup ──
app = FastAPI(title="Nathan's API")

# ── Database Connection ──
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL environment variable is not set!")

engine = create_engine(DATABASE_URL)

# ── Valid views (read-only) ──
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
    "pending_assignments_summary",
}

# ── Raw tables (auto-generated endpoints) ──
RAW_TABLES = [
    "people",
    "companies",
    "deals",
    "budgets",
    "projects",
    "project_assignments",
    "service_assignments",
    "services",
    "time_entries",
    "custom_fields",
    "custom_field_options",
]

# ── Root health-check ──
@app.get("/")
def root():
    return {"message": "✅ Nathan API is live and connected!"}

# ── View endpoints ──
@app.get("/views/{view_name}")
def read_view(view_name: str):
    if view_name not in VALID_VIEWS:
        raise HTTPException(status_code=400, detail="❌ Invalid view name")
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {view_name}"))
            rows = [dict(r) for r in result.mappings().all()]
        return {"rows": rows}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"❌ Database error: {e}")

# ── Raw table endpoints ──
router = APIRouter(prefix="/raw", tags=["raw"])

for table in RAW_TABLES:
    async def read_table(table_name=table):
        try:
            with engine.connect() as conn:
                result = conn.execute(text(f"SELECT * FROM {table_name}"))
                data = [dict(r) for r in result.mappings().all()]
            return JSONResponse(content=data)
        except SQLAlchemyError as e:
            return JSONResponse(status_code=500, content={"error": f"❌ Error reading {table_name}: {e}"})

    router.add_api_route(f"/{table}", read_table, methods=["GET"])

app.include_router(router)
