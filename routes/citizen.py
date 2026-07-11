"""
Citizen API routes — reads from MongoDB Atlas.
"""
from fastapi import APIRouter
from datetime import date
from db.mongo_client import undertrials_col, hearings_col

router = APIRouter(prefix="/citizen", tags=["citizen"])


def days_in_custody(arrest_date_str: str) -> int:
    try:
        arrest = date.fromisoformat(str(arrest_date_str))
        return (date.today() - arrest).days
    except Exception:
        return 0


def get_alert_status(days: int) -> str:
    if days > 90:
        return "red"
    if days > 60:
        return "yellow"
    return "green"


def clean(doc: dict) -> dict:
    """Remove MongoDB _id field so it's JSON serializable."""
    doc.pop("_id", None)
    return doc


@router.get("/status/search")
async def search_prisoner(q: str = ""):
    if not q.strip():
        return {"found": False, "results": [], "count": 0}

    try:
        q_lower = q.lower()
        # Search by prisoner_id OR name (case-insensitive)
        results = list(undertrials_col.find({
            "$or": [
                {"prisoner_id": {"$regex": q_lower, "$options": "i"}},
                {"name": {"$regex": q_lower, "$options": "i"}}
            ]
        }))

        if not results:
            return {"found": False, "results": [], "count": 0}

        enriched = []
        for p in results:
            p = clean(p)
            days = days_in_custody(p["arrest_date"])
            hearings = [clean(h) for h in hearings_col.find({"prisoner_id": p["prisoner_id"]}).sort("hearing_date", 1)]
            enriched.append({
                **p,
                "days_in_custody": days,
                "alert_status": get_alert_status(days),
                "hearings": hearings
            })

        return {"found": True, "count": len(enriched), "results": enriched}

    except Exception as e:
        print(f"Search error: {e}")
        return {"found": False, "results": [], "count": 0, "error": str(e)}


@router.get("/status/{prisoner_id}")
async def get_prisoner_status(prisoner_id: str):
    try:
        p = undertrials_col.find_one({"prisoner_id": prisoner_id})
        if not p:
            return {"found": False}

        p = clean(p)
        days = days_in_custody(p["arrest_date"])
        hearings = [clean(h) for h in hearings_col.find({"prisoner_id": prisoner_id}).sort("hearing_date", 1)]

        return {
            "found": True,
            "prisoner": {
                **p,
                "days_in_custody": days,
                "alert_status": get_alert_status(days),
                "hearings": hearings
            }
        }
    except Exception as e:
        print(f"Get prisoner error: {e}")
        return {"found": False, "error": str(e)}


@router.get("/calendar/{prisoner_id}")
async def get_court_calendar(prisoner_id: str):
    try:
        p = undertrials_col.find_one({"prisoner_id": prisoner_id})
        if not p:
            return {"found": False}

        p = clean(p)
        days = days_in_custody(p["arrest_date"])
        hearings = [clean(h) for h in hearings_col.find({"prisoner_id": prisoner_id}).sort("hearing_date", 1)]

        next_hearing_str = p.get("next_hearing")
        days_until = 0
        if next_hearing_str:
            try:
                next_hearing = date.fromisoformat(next_hearing_str)
                days_until = (next_hearing - date.today()).days
            except Exception:
                days_until = 0

        return {
            "found": True,
            "case": {
                "prisoner_name": p["name"],
                "prisoner_id": p["prisoner_id"],
                "case_status": p["case_status"],
                "court": p["court"],
                "charges": p["charges"],
                "next_hearing_date": next_hearing_str,
                "days_until_hearing": days_until,
                "days_in_custody": days,
                "hearings": hearings
            }
        }
    except Exception as e:
        print(f"Calendar error: {e}")
        return {"found": False, "error": str(e)}