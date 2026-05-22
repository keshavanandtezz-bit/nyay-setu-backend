import os
import json
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import pdfplumber
import tempfile

load_dotenv()

router = APIRouter(prefix="/ai", tags=["ai"])

GROQ_KEY = os.getenv("GROQ_API_KEY", "")
MODEL = "llama-3.3-70b-versatile"


def get_groq_client():
    if not GROQ_KEY:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY not set in environment variables"
        )
    return Groq(api_key=GROQ_KEY)


class ChatMessage(BaseModel):
    messages: list
    system_prompt: str = ""


class BailRequest(BaseModel):
    prisoner_name: str
    age: int
    prisoner_id: str
    charges: str
    ipc_sections: str
    court: str
    district: str
    arrest_date: str
    days_in_custody: int
    has_prior_record: bool
    case_status: str
    lawyer: str


@router.get("/check-key")
async def check_key():
    """Check if Groq key is configured correctly"""
    if not GROQ_KEY:
        return {"status": "error", "message": "GROQ_API_KEY not set"}
    if len(GROQ_KEY) < 20:
        return {"status": "error", "message": "GROQ_API_KEY looks invalid (too short)"}
    return {
        "status": "ok",
        "key_prefix": GROQ_KEY[:8] + "...",
        "key_length": len(GROQ_KEY)
    }


@router.post("/rights-bot")
async def rights_bot(payload: ChatMessage):
    try:
        client = get_groq_client()

        system = payload.system_prompt or (
            "You are Nyay Sahayak, a legal rights assistant for Indian citizens. "
            "Explain Indian laws and rights in simple plain English. "
            "Never give specific legal advice — always suggest consulting a lawyer. "
            "Keep answers under 200 words. Use bullet points for lists. "
            "When relevant mention free legal aid helpline: 15100. "
            "Focus on: IPC, CrPC, bail rights, undertrial rights, FIR procedures."
        )

        messages = [{"role": "system", "content": system}]
        for m in payload.messages:
            if isinstance(m, dict):
                messages.append(m)

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        error_msg = str(e)
        print(f"RightsBot error: {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/analyze-case")
async def analyze_case(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files accepted")

    try:
        content = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        full_text = ""
        with pdfplumber.open(tmp_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

        if not full_text.strip():
            raise HTTPException(
                status_code=400,
                detail="PDF appears scanned. Please use a searchable PDF."
            )

        words = full_text.split()[:3500]
        truncated = " ".join(words)
        result = await _analyze_text_internal(truncated)
        return {"success": True, "analysis": result}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-text")
async def analyze_text_endpoint(payload: dict):
    try:
        text = payload.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="No text provided")
        words = text.split()[:3500]
        truncated = " ".join(words)
        result = await _analyze_text_internal(truncated)
        return {"success": True, "analysis": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def _analyze_text_internal(case_text: str) -> dict:
    client = get_groq_client()
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=1500,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Nyay Mitra, an AI legal assistant for Indian courts. "
                    "Analyze the case document and return ONLY valid JSON. "
                    "No extra text, no markdown, no backticks. "
                    'Use this exact structure: {"case_title":"","case_number":"",'
                    '"court":"","judge":"","accused":[],"charges":[],'
                    '"ipc_sections":[],"bail_status":"","current_status":"",'
                    '"key_facts":[],"important_dates":[],"summary":"",'
                    '"next_hearing":"","witnesses_total":0,"witnesses_examined":0}'
                )
            },
            {
                "role": "user",
                "content": f"Analyze this Indian court document:\n\n{case_text}"
            }
        ]
    )
    raw = response.choices[0].message.content
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


@router.post("/generate-bail")
async def generate_bail_application(payload: BailRequest):
    try:
        client = get_groq_client()
        from datetime import date
        today = date.today().strftime("%d %B %Y")

        response = client.chat.completions.create(
            model=MODEL,
            max_tokens=1500,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert Indian criminal lawyer. "
                        "Generate formal professional bail applications "
                        "for Indian courts under CrPC Section 437 or 439. "
                        "Return only the bail application text, properly formatted."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Generate a complete formal bail application:\n\n"
                        f"Name: {payload.prisoner_name}\n"
                        f"Age: {payload.age} years\n"
                        f"Prisoner ID: {payload.prisoner_id}\n"
                        f"Charges: {payload.charges}\n"
                        f"IPC Sections: {payload.ipc_sections}\n"
                        f"Court: {payload.court}\n"
                        f"District: {payload.district}\n"
                        f"Date of Arrest: {payload.arrest_date}\n"
                        f"Days in Custody: {payload.days_in_custody} days\n"
                        f"Prior Criminal Record: {'Yes' if payload.has_prior_record else 'No'}\n"
                        f"Current Status: {payload.case_status}\n"
                        f"Legal Representation: {payload.lawyer}\n"
                        f"Today's Date: {today}\n\n"
                        f"Write a complete bail application with court header, "
                        f"grounds for bail emphasizing {payload.days_in_custody} days "
                        f"in custody, Article 21 rights, prayer clause, and verification."
                    )
                }
            ]
        )
        return {"success": True, "application": response.choices[0].message.content}

    except Exception as e:
        error_msg = str(e)
        print(f"Bail generation error: {error_msg}")
        raise HTTPException(status_code=500, detail=error_msg)