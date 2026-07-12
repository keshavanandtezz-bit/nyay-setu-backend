"""
Case API routes — handles complaint filing, case lookup, and stage tracking.
Uses MongoDB Atlas for persistence.
"""
import os
import uuid
from datetime import datetime, date
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from db.mongo_client import db

router = APIRouter(prefix="/case", tags=["case"])

# Collection for filed complaints / cases
cases_col = db["cases"]


def clean(doc: dict) -> dict:
    """Remove MongoDB _id field so it's JSON serializable."""
    if doc:
        doc.pop("_id", None)
    return doc


# ── Pydantic models ──────────────────────────────────────────────────────────

class ComplaintData(BaseModel):
    description: str
    category: str
    incident_date: str
    location: str
    district: str
    complainant_name: str
    phone: str
    email: Optional[str] = ""
    accused_name: Optional[str] = ""
    evidence_description: Optional[str] = ""
    ai_summary: Optional[str] = ""
    suggested_ipc: Optional[List] = []


class StageUpdate(BaseModel):
    stage: str
    notes: Optional[str] = ""


class DocumentMeta(BaseModel):
    filename: str
    type: str
    description: Optional[str] = ""


# ── Routes ───────────────────────────────────────────────────────────────────

@router.post("/file-complaint")
async def file_complaint(data: ComplaintData):
    """File a new complaint and store it in MongoDB."""
    try:
        # Generate a unique case ID in format NS-YYYY-XXXXXX
        year = datetime.now().year
        unique_part = str(uuid.uuid4()).upper()[:6]
        case_id = f"NS-{year}-{unique_part}"

        case_doc = {
            "case_id": case_id,
            "status": "Registered",
            "stage": "complaint_filed",
            "filed_at": datetime.utcnow().isoformat(),
            "last_updated": datetime.utcnow().isoformat(),
            "description": data.description,
            "category": data.category,
            "incident_date": data.incident_date,
            "location": data.location,
            "district": data.district,
            "complainant_name": data.complainant_name,
            "phone": data.phone,
            "email": data.email or "",
            "accused_name": data.accused_name or "",
            "evidence_description": data.evidence_description or "",
            "ai_summary": data.ai_summary or "",
            "suggested_ipc": data.suggested_ipc or [],
            "documents": [],
            "stage_history": [
                {
                    "stage": "complaint_filed",
                    "label": "Complaint Filed",
                    "completed_at": datetime.utcnow().isoformat(),
                    "notes": "Complaint successfully registered via Nyay Setu."
                }
            ]
        }

        cases_col.insert_one(case_doc)
        clean(case_doc)

        return {
            "success": True,
            "case_id": case_id,
            "message": f"Complaint registered. Your Case ID is {case_id}. Please save this for future tracking.",
            "status": "Registered"
        }

    except Exception as e:
        print(f"File complaint error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to file complaint: {str(e)}")


@router.get("/{case_id}")
async def get_case(case_id: str):
    """Fetch a case by its case ID."""
    try:
        doc = cases_col.find_one({"case_id": case_id.upper()})
        if not doc:
            return {"found": False, "message": f"No case found with ID: {case_id}"}
        return {"found": True, "case": clean(doc)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_cases(phone: str = "", name: str = ""):
    """Search for cases by phone or complainant name."""
    try:
        query = {}
        if phone:
            query["phone"] = {"$regex": phone.strip(), "$options": "i"}
        elif name:
            query["complainant_name"] = {"$regex": name.strip(), "$options": "i"}
        else:
            return {"found": False, "results": [], "count": 0}

        docs = list(cases_col.find(query).sort("filed_at", -1).limit(20))
        results = [clean(d) for d in docs]
        return {"found": len(results) > 0, "count": len(results), "results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{case_id}/stage")
async def update_stage(case_id: str, body: StageUpdate):
    """Update the current stage of a case."""
    try:
        case_id = case_id.upper()
        doc = cases_col.find_one({"case_id": case_id})
        if not doc:
            raise HTTPException(status_code=404, detail=f"Case {case_id} not found")

        stage_entry = {
            "stage": body.stage,
            "label": body.stage.replace("_", " ").title(),
            "completed_at": datetime.utcnow().isoformat(),
            "notes": body.notes or ""
        }

        cases_col.update_one(
            {"case_id": case_id},
            {
                "$set": {
                    "stage": body.stage,
                    "last_updated": datetime.utcnow().isoformat()
                },
                "$push": {"stage_history": stage_entry}
            }
        )
        return {"success": True, "case_id": case_id, "new_stage": body.stage}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{case_id}/documents")
async def add_document(case_id: str, meta: DocumentMeta):
    """Add a document reference to a case."""
    try:
        case_id = case_id.upper()
        doc_entry = {
            "filename": meta.filename,
            "type": meta.type,
            "description": meta.description or "",
            "uploaded_at": datetime.utcnow().isoformat()
        }
        result = cases_col.update_one(
            {"case_id": case_id},
            {"$push": {"documents": doc_entry}}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
        return {"success": True, "document": doc_entry}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{case_id}/documents")
async def get_documents(case_id: str):
    """Get all documents for a case."""
    try:
        doc = cases_col.find_one({"case_id": case_id.upper()})
        if not doc:
            raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
        return {"case_id": case_id.upper(), "documents": doc.get("documents", [])}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics")
async def get_analytics():
    """Basic analytics across all filed cases."""
    try:
        total = cases_col.count_documents({})
        by_category = list(cases_col.aggregate([
            {"$group": {"_id": "$category", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]))
        by_district = list(cases_col.aggregate([
            {"$group": {"_id": "$district", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]))
        return {
            "total_cases": total,
            "by_category": [{"category": x["_id"], "count": x["count"]} for x in by_category],
            "by_district": [{"district": x["_id"], "count": x["count"]} for x in by_district]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
