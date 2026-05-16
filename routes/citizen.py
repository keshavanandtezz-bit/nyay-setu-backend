from fastapi import APIRouter
from datetime import date
from db.supabase_client import supabase

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


@router.get("/status/search")
async def search_prisoner(q: str = ""):
    if not q.strip():
        return {"found": False, "results": [], "count": 0}

    try:
        id_result = supabase.table("undertrials") \
            .select("*") \
            .ilike("prisoner_id", f"%{q}%") \
            .execute()

        name_result = supabase.table("undertrials") \
            .select("*") \
            .ilike("name", f"%{q}%") \
            .execute()

        all_records = list(id_result.data or [])
        seen_ids = {r["prisoner_id"] for r in all_records}
        for r in (name_result.data or []):
            if r["prisoner_id"] not in seen_ids:
                all_records.append(r)
                seen_ids.add(r["prisoner_id"])

        if not all_records:
            return {"found": False, "results": [], "count": 0}

        enriched = []
        for p in all_records:
            days = days_in_custody(p["arrest_date"])
            hearings_result = supabase.table("hearings") \
                .select("*") \
                .eq("prisoner_id", p["prisoner_id"]) \
                .order("hearing_date") \
                .execute()

            enriched.append({
                **p,
                "days_in_custody": days,
                "alert_status": get_alert_status(days),
                "hearings": hearings_result.data or []
            })

        return {
            "found": True,
            "count": len(enriched),
            "results": enriched
        }

    except Exception as e:
        print(f"Search error: {e}")
        return {"found": False, "results": [], "count": 0, "error": str(e)}


@router.get("/status/{prisoner_id}")
async def get_prisoner_status(prisoner_id: str):
    try:
        result = supabase.table("undertrials") \
            .select("*") \
            .eq("prisoner_id", prisoner_id) \
            .execute()

        if not result.data:
            return {"found": False}

        p = result.data[0]
        days = days_in_custody(p["arrest_date"])

        hearings_result = supabase.table("hearings") \
            .select("*") \
            .eq("prisoner_id", prisoner_id) \
            .order("hearing_date") \
            .execute()

        return {
            "found": True,
            "prisoner": {
                **p,
                "days_in_custody": days,
                "alert_status": get_alert_status(days),
                "hearings": hearings_result.data or []
            }
        }

    except Exception as e:
        print(f"Get prisoner error: {e}")
        return {"found": False, "error": str(e)}


@router.get("/calendar/{prisoner_id}")
async def get_court_calendar(prisoner_id: str):
    try:
        p_result = supabase.table("undertrials") \
            .select("*") \
            .eq("prisoner_id", prisoner_id) \
            .execute()

        if not p_result.data:
            return {"found": False}

        p = p_result.data[0]
        days = days_in_custody(p["arrest_date"])

        hearings_result = supabase.table("hearings") \
            .select("*") \
            .eq("prisoner_id", prisoner_id) \
            .order("hearing_date") \
            .execute()

        next_hearing_str = str(p["next_hearing"]) if p.get("next_hearing") else None
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
                "hearings": hearings_result.data or []
            }
        }

    except Exception as e:
        print(f"Calendar error: {e}")
        return {"found": False, "error": str(e)}