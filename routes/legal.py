"""
Legal API routes — reads from MongoDB Atlas.
"""
from fastapi import APIRouter
from datetime import date
from db.mongo_client import undertrials_col, hearings_col, legal_aid_col, precedents_col

router = APIRouter(prefix="/legal", tags=["legal"])


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


def get_bail_score(prisoner: dict) -> int:
    score = 50
    offense_map = {"minor": 20, "bailable": 10, "non-bailable": -15, "heinous": -30}
    score += offense_map.get(prisoner.get("offense_type", ""), 0)

    days = days_in_custody(prisoner["arrest_date"])
    if days > 300: score += 20
    elif days > 180: score += 15
    elif days > 90: score += 10
    elif days > 60: score += 5

    if prisoner.get("prior_record"): score -= 20
    if not prisoner.get("has_lawyer"): score += 8

    flight_map = {"low": 10, "medium": 0, "high": -20}
    score += flight_map.get(prisoner.get("flight_risk", ""), 0)

    return max(0, min(100, score))


def clean(doc: dict) -> dict:
    doc.pop("_id", None)
    return doc


@router.get("/undertrials")
async def get_all_undertrials(status: str = "all", district: str = ""):
    try:
        query = {}
        if district:
            query["district"] = district

        prisoners = [clean(p) for p in undertrials_col.find(query)]

        enriched = []
        for p in prisoners:
            days = days_in_custody(p["arrest_date"])
            alert = get_alert_status(days)
            if status != "all" and alert != status:
                continue
            enriched.append({**p, "days_in_custody": days, "alert_status": alert, "bail_score": get_bail_score(p)})

        priority = {"red": 0, "yellow": 1, "green": 2}
        enriched.sort(key=lambda x: (priority[x["alert_status"]], -x["days_in_custody"]))

        counts = {
            "total": len(enriched),
            "red": sum(1 for u in enriched if u["alert_status"] == "red"),
            "yellow": sum(1 for u in enriched if u["alert_status"] == "yellow"),
            "green": sum(1 for u in enriched if u["alert_status"] == "green"),
        }

        return {"success": True, "counts": counts, "undertrials": enriched}

    except Exception as e:
        return {"success": False, "error": str(e), "undertrials": []}


@router.get("/undertrial/{undertrial_id}")
async def get_undertrial(undertrial_id: str):
    try:
        p = undertrials_col.find_one({"prisoner_id": undertrial_id})
        if not p:
            return {"found": False}
        p = clean(p)
        days = days_in_custody(p["arrest_date"])
        return {
            "found": True,
            "prisoner": {**p, "days_in_custody": days, "alert_status": get_alert_status(days), "bail_score": get_bail_score(p)}
        }
    except Exception as e:
        return {"found": False, "error": str(e)}


@router.get("/districts")
async def get_districts():
    try:
        districts = sorted(undertrials_col.distinct("district"))
        return {"districts": districts}
    except Exception as e:
        return {"districts": [], "error": str(e)}


@router.get("/stats")
async def get_dashboard_stats():
    try:
        prisoners = [clean(p) for p in undertrials_col.find({})]
        total = len(prisoners)
        overdue = sum(1 for p in prisoners if days_in_custody(p["arrest_date"]) > 90)
        approaching = sum(1 for p in prisoners if 60 < days_in_custody(p["arrest_date"]) <= 90)
        no_lawyer = sum(1 for p in prisoners if not p.get("has_lawyer"))
        return {
            "total_undertrials": total,
            "overdue_count": overdue,
            "approaching_limit": approaching,
            "no_lawyer_assigned": no_lawyer,
        }
    except Exception as e:
        return {"error": str(e)}


@router.get("/legal-aid")
async def get_legal_aid(district: str = ""):
    try:
        query = {}
        if district:
            query["district"] = {"$regex": district, "$options": "i"}
        providers = [clean(p) for p in legal_aid_col.find(query)]
        return {"success": True, "count": len(providers), "providers": providers}
    except Exception as e:
        return {"success": False, "error": str(e), "providers": []}


@router.get("/precedents")
async def get_precedents(category: str = "", q: str = ""):
    try:
        query = {}
        if category:
            query["category"] = {"$regex": category, "$options": "i"}
        if q:
            query["$or"] = [
                {"title": {"$regex": q, "$options": "i"}},
                {"summary": {"$regex": q, "$options": "i"}},
                {"ipc_sections": {"$regex": q, "$options": "i"}},
            ]
        results = [clean(p) for p in precedents_col.find(query)]
        return {"success": True, "count": len(results), "precedents": results}
    except Exception as e:
        return {"success": False, "error": str(e), "precedents": []}