import os
import json
import tempfile
from datetime import date
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import pdfplumber

load_dotenv()

router = APIRouter(prefix="/ai", tags=["ai"])

GROQ_KEY = os.getenv("GROQ_API_KEY", "")
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
MAX_PDF_SIZE_MB = 10


def get_groq_client():
    if not GROQ_KEY:
        raise HTTPException(
            status_code=500,
            detail="AI service is not configured. Please contact support."
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
            if isinstance(m, dict) and "role" in m and "content" in m:
                messages.append(m)

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        return {"reply": reply}

    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        print(f"RightsBot error: {error_msg}")
        raise HTTPException(status_code=500, detail="AI service is temporarily unavailable. Please try again.")


@router.post("/analyze-case")
async def analyze_case(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files accepted")

    content = await file.read()
    if len(content) > MAX_PDF_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"File too large. Maximum size is {MAX_PDF_SIZE_MB}MB.")

    tmp_path = None
    try:
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
                detail="PDF appears to be scanned (image-based). Please use a text-searchable PDF."
            )

        words = full_text.split()[:3500]
        truncated = " ".join(words)
        result = await _analyze_text_internal(truncated)
        return {"success": True, "analysis": result}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except Exception:
                pass


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
    cleaned = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback: return a safe empty structure if LLM returns invalid JSON
        return {
            "case_title": "Analysis Complete",
            "case_number": "",
            "court": "",
            "judge": "",
            "accused": [],
            "charges": [],
            "ipc_sections": [],
            "bail_status": "Unknown",
            "current_status": "See summary below",
            "key_facts": [],
            "important_dates": [],
            "summary": cleaned[:1000] if cleaned else "Could not parse structured analysis.",
            "next_hearing": "",
            "witnesses_total": 0,
            "witnesses_examined": 0
        }


@router.post("/generate-bail")
async def generate_bail_application(payload: BailRequest):
    try:
        client = get_groq_client()
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

    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        print(f"Bail generation error: {error_msg}")
        raise HTTPException(status_code=500, detail="AI service is temporarily unavailable. Please try again.")