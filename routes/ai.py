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
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"


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
    """AI chatbot for legal rights questions"""
    try:
        system = payload.system_prompt or """You are Nyay Sahayak, a compassionate legal rights
assistant for Indian citizens. Explain Indian laws and rights in simple plain English.
Never give specific legal advice — always suggest consulting a lawyer.
Keep answers under 200 words. Use bullet points for lists.
When relevant, mention free legal aid helpline: 15100.
Focus on: IPC, CrPC, bail rights, undertrial rights, FIR procedures, legal aid, NDPS, domestic violence."""

        response = groq_client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": system}] + payload.messages,
            max_tokens=500,
            temperature=0.7
        )
        return {"reply": response.choices[0].message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-case")
async def analyze_case(file: UploadFile = File(...)):
    """Extract text from PDF and analyze case with AI"""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

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
            raise HTTPException(status_code=400,
                detail="PDF appears to be scanned. Please use a searchable PDF.")

        words = full_text.split()[:3500]
        truncated = " ".join(words)

        result = await _analyze_text(truncated)
        return {"success": True, "analysis": result}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-text")
async def analyze_text_endpoint(payload: dict):
    """Analyze raw case text (for sample case demo)"""
    try:
        text = payload.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="No text provided")

        words = text.split()[:3500]
        truncated = " ".join(words)
        result = await _analyze_text(truncated)
        return {"success": True, "analysis": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def _analyze_text(case_text: str) -> dict:
    response = groq_client.chat.completions.create(
        model=MODEL,
        max_tokens=1500,
        messages=[
            {
                "role": "system",
                "content": """You are Nyay Mitra, an AI legal assistant for Indian courts.
Analyze the case document and return ONLY valid JSON with no extra text, no markdown, no backticks.
Use this exact structure:
{
  "case_title": "Short title like State vs. Accused Name",
  "case_number": "Full case number",
  "court": "Name of court",
  "judge": "Judge name or Unknown",
  "accused": ["Name 1", "Name 2"],
  "charges": ["Charge 1", "Charge 2"],
  "ipc_sections": ["IPC 420", "IPC 406"],
  "bail_status": "Denied / Granted / Not Applied",
  "current_status": "Current stage of trial",
  "key_facts": ["Fact 1", "Fact 2", "Fact 3", "Fact 4", "Fact 5"],
  "important_dates": [{"event": "FIR Filed", "date": "DD.MM.YYYY"}],
  "summary": "3 sentence plain English summary for a judge preparing for hearing.",
  "next_hearing": "DD.MM.YYYY or Unknown",
  "witnesses_total": 0,
  "witnesses_examined": 0
}"""
            },
            {"role": "user", "content": f"Analyze this Indian court document:\n\n{case_text}"}
        ]
    )
    raw = response.choices[0].message.content
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


@router.post("/generate-bail")
async def generate_bail_application(payload: BailRequest):
    """Generate a complete bail application document"""
    try:
        from datetime import date
        today = date.today().strftime("%d %B %Y")

        response = groq_client.chat.completions.create(
            model=MODEL,
            max_tokens=1500,
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert Indian criminal lawyer. Generate a formal,
professional bail application for an Indian court. Use proper legal language, formatting, and
structure. Include all standard sections of an Indian bail application under CrPC Section 437
or 439. Return only the bail application text, properly formatted."""
                },
                {
                    "role": "user",
                    "content": f"""Generate a complete formal bail application:

Name: {payload.prisoner_name}
Age: {payload.age} years
Prisoner ID: {payload.prisoner_id}
Charges: {payload.charges}
IPC Sections: {payload.ipc_sections}
Court: {payload.court}
District: {payload.district}
Date of Arrest: {payload.arrest_date}
Days in Custody: {payload.days_in_custody} days
Prior Criminal Record: {'Yes' if payload.has_prior_record else 'No'}
Current Status: {payload.case_status}
Legal Representation: {payload.lawyer}
Today's Date: {today}

Generate a complete bail application with: court header, application number placeholder,
grounds for bail (emphasizing {payload.days_in_custody} days of custody, personal liberty
under Article 21, no flight risk), prayer clause, and verification."""
                }
            ]
        )
        return {
            "success": True,
            "application": response.choices[0].message.content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))