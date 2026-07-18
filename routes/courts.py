"""
Courts API — returns court locations for CourtFinder.js
"""
from fastapi import APIRouter
from db.mongo_client import courts_col

router = APIRouter(prefix="/courts", tags=["courts"])


def clean(doc: dict) -> dict:
    doc.pop("_id", None)
    return doc


@router.get("")
async def find_courts(district: str = "", court_type: str = ""):
    """Find courts by district and/or type."""
    try:
        query = {}
        if district:
            query["district"] = {"$regex": district, "$options": "i"}
        if court_type:
            query["court_type"] = {"$regex": court_type, "$options": "i"}
        courts = [clean(c) for c in courts_col.find(query).sort("name", 1)]
        return {"success": True, "count": len(courts), "courts": courts}
    except Exception as e:
        return {"success": False, "error": str(e), "courts": []}


@router.get("/districts")
async def get_court_districts():
    """Get list of all distinct districts that have courts."""
    try:
        districts = sorted(courts_col.distinct("district"))
        return {"districts": districts}
    except Exception as e:
        return {"districts": [], "error": str(e)}


@router.get("/types")
async def get_court_types():
    """Get list of all distinct court types."""
    try:
        types = sorted(courts_col.distinct("court_type"))
        return {"types": types}
    except Exception as e:
        return {"types": [], "error": str(e)}
