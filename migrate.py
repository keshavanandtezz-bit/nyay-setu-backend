"""
Migration script — seeds MongoDB with all Nyay Setu data.
Run once: python migrate.py
"""
import os
from datetime import date
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "")
client = MongoClient(MONGODB_URI)
db = client["nyaysetu"]

# ── 1. UNDERTRIALS ────────────────────────────────────────────────────
undertrials = [
    {"prisoner_id": "KA-BLR-2024-001", "name": "Raju Sharma", "age": 34, "charges": "Theft & Robbery", "ipc_sections": "IPC 379, IPC 392", "arrest_date": "2024-01-15", "court": "City Civil & Sessions Court", "district": "Bengaluru Urban", "case_status": "Under Trial", "next_hearing": "2025-08-10", "lawyer": "Adv. Meena Rao", "has_lawyer": True, "prior_record": False, "offense_type": "non-bailable", "flight_risk": "medium", "prison": "Parappana Agrahara Central Prison"},
    {"prisoner_id": "KA-MYS-2024-002", "name": "Suresh Kumar", "age": 28, "charges": "Assault & Battery", "ipc_sections": "IPC 323, IPC 325", "arrest_date": "2024-03-22", "court": "District & Sessions Court, Mysuru", "district": "Mysuru", "case_status": "Bail Pending", "next_hearing": "2025-07-25", "lawyer": "None assigned", "has_lawyer": False, "prior_record": True, "offense_type": "bailable", "flight_risk": "low", "prison": "Mysuru Central Prison"},
    {"prisoner_id": "KA-HUB-2024-003", "name": "Anand Patil", "age": 45, "charges": "Murder", "ipc_sections": "IPC 302", "arrest_date": "2023-11-05", "court": "Sessions Court, Hubballi", "district": "Dharwad", "case_status": "Trial in Progress", "next_hearing": "2025-08-01", "lawyer": "Adv. Rakesh Shetty", "has_lawyer": True, "prior_record": True, "offense_type": "heinous", "flight_risk": "high", "prison": "Hubballi Central Prison"},
    {"prisoner_id": "KA-MGR-2024-004", "name": "Priya Nair", "age": 31, "charges": "Fraud & Cheating", "ipc_sections": "IPC 420, IPC 406", "arrest_date": "2024-05-10", "court": "District Court, Mangaluru", "district": "Dakshina Kannada", "case_status": "Bail Pending", "next_hearing": "2025-07-30", "lawyer": "Adv. Anjali Bhat", "has_lawyer": True, "prior_record": False, "offense_type": "bailable", "flight_risk": "low", "prison": "Mangaluru Sub-Jail"},
    {"prisoner_id": "KA-BLR-2024-005", "name": "Mohan Das", "age": 52, "charges": "Drug Trafficking", "ipc_sections": "NDPS Act Sec 21, 29", "arrest_date": "2023-08-18", "court": "Special NDPS Court, Bengaluru", "district": "Bengaluru Urban", "case_status": "Under Trial", "next_hearing": "2025-08-15", "lawyer": "Adv. Sunil Kumar", "has_lawyer": True, "prior_record": True, "offense_type": "non-bailable", "flight_risk": "high", "prison": "Parappana Agrahara Central Prison"},
    {"prisoner_id": "KA-KLR-2024-006", "name": "Fatima Begum", "age": 38, "charges": "Domestic Violence", "ipc_sections": "IPC 498A, IPC 323", "arrest_date": "2024-07-01", "court": "Judicial Magistrate Court, Kalaburagi", "district": "Kalaburagi", "case_status": "Bail Pending", "next_hearing": "2025-08-05", "lawyer": "None assigned", "has_lawyer": False, "prior_record": False, "offense_type": "bailable", "flight_risk": "low", "prison": "Kalaburagi District Prison"},
    {"prisoner_id": "KA-BLR-2024-007", "name": "Venkat Reddy", "age": 41, "charges": "Corruption & Bribery", "ipc_sections": "IPC 161, IPC 165, Prevention of Corruption Act", "arrest_date": "2023-06-12", "court": "Special CBI Court, Bengaluru", "district": "Bengaluru Urban", "case_status": "Trial in Progress", "next_hearing": "2025-07-28", "lawyer": "Adv. Pradeep Nair", "has_lawyer": True, "prior_record": False, "offense_type": "non-bailable", "flight_risk": "medium", "prison": "Parappana Agrahara Central Prison"},
    {"prisoner_id": "KA-MNG-2024-008", "name": "Arjun Singh", "age": 25, "charges": "Cybercrime", "ipc_sections": "IT Act 66, 66C, 66D", "arrest_date": "2024-09-15", "court": "Cyber Crime Court, Mangaluru", "district": "Dakshina Kannada", "case_status": "Under Trial", "next_hearing": "2025-08-20", "lawyer": "Adv. Deepa Shetty", "has_lawyer": True, "prior_record": False, "offense_type": "bailable", "flight_risk": "low", "prison": "Mangaluru Sub-Jail"},
    {"prisoner_id": "KA-BLR-2024-009", "name": "Kavitha Reddy", "age": 29, "charges": "Kidnapping", "ipc_sections": "IPC 363, IPC 366", "arrest_date": "2024-02-28", "court": "City Civil & Sessions Court", "district": "Bengaluru Urban", "case_status": "Under Trial", "next_hearing": "2025-08-12", "lawyer": "Adv. Ramesh Kumar", "has_lawyer": True, "prior_record": False, "offense_type": "non-bailable", "flight_risk": "medium", "prison": "Parappana Agrahara Central Prison"},
    {"prisoner_id": "KA-BLR-2024-010", "name": "Syed Mohammed", "age": 35, "charges": "Arms Act Violation", "ipc_sections": "Arms Act Sec 25, 27", "arrest_date": "2023-12-10", "court": "Additional Sessions Court, Bengaluru", "district": "Bengaluru Urban", "case_status": "Trial in Progress", "next_hearing": "2025-07-22", "lawyer": "Adv. Farhana Sheikh", "has_lawyer": True, "prior_record": True, "offense_type": "non-bailable", "flight_risk": "high", "prison": "Parappana Agrahara Central Prison"},
]

# ── 2. HEARINGS ───────────────────────────────────────────────────────
hearings = [
    {"prisoner_id": "KA-BLR-2024-001", "hearing_date": "2024-03-15", "purpose": "Charge framing", "result": "Charges framed", "next_date": "2024-06-20", "judge": "Hon. Justice Ramaiah"},
    {"prisoner_id": "KA-BLR-2024-001", "hearing_date": "2024-06-20", "purpose": "Evidence recording", "result": "Prosecution witness examined", "next_date": "2024-09-10", "judge": "Hon. Justice Ramaiah"},
    {"prisoner_id": "KA-BLR-2024-001", "hearing_date": "2024-09-10", "purpose": "Cross examination", "result": "Adjourned", "next_date": "2025-08-10", "judge": "Hon. Justice Ramaiah"},
    {"prisoner_id": "KA-MYS-2024-002", "hearing_date": "2024-05-01", "purpose": "Bail application", "result": "Bail rejected", "next_date": "2025-07-25", "judge": "Hon. Justice Krishnaswamy"},
    {"prisoner_id": "KA-HUB-2024-003", "hearing_date": "2024-02-10", "purpose": "Remand hearing", "result": "Remanded to judicial custody", "next_date": "2024-05-15", "judge": "Hon. Justice Patil"},
    {"prisoner_id": "KA-HUB-2024-003", "hearing_date": "2024-05-15", "purpose": "Charge framing", "result": "Charges framed", "next_date": "2025-08-01", "judge": "Hon. Justice Patil"},
    {"prisoner_id": "KA-MGR-2024-004", "hearing_date": "2024-06-20", "purpose": "Bail hearing", "result": "Bail under consideration", "next_date": "2025-07-30", "judge": "Hon. Justice Bhat"},
    {"prisoner_id": "KA-BLR-2024-005", "hearing_date": "2023-10-05", "purpose": "Remand", "result": "Remanded", "next_date": "2024-01-15", "judge": "Hon. Justice Nair"},
    {"prisoner_id": "KA-BLR-2024-005", "hearing_date": "2024-01-15", "purpose": "Charge framing", "result": "Charges framed", "next_date": "2024-06-10", "judge": "Hon. Justice Nair"},
    {"prisoner_id": "KA-BLR-2024-005", "hearing_date": "2024-06-10", "purpose": "Evidence", "result": "Witness examined", "next_date": "2025-08-15", "judge": "Hon. Justice Nair"},
    {"prisoner_id": "KA-KLR-2024-006", "hearing_date": "2024-08-15", "purpose": "Bail application", "result": "Adjourned", "next_date": "2025-08-05", "judge": "Hon. Justice Shaikh"},
    {"prisoner_id": "KA-BLR-2024-007", "hearing_date": "2023-08-20", "purpose": "Charge framing", "result": "Charges framed", "next_date": "2024-02-15", "judge": "Hon. Justice Verma"},
    {"prisoner_id": "KA-BLR-2024-007", "hearing_date": "2024-02-15", "purpose": "Evidence recording", "result": "Documents submitted", "next_date": "2025-07-28", "judge": "Hon. Justice Verma"},
    {"prisoner_id": "KA-MNG-2024-008", "hearing_date": "2024-11-01", "purpose": "Charge framing", "result": "Charges framed", "next_date": "2025-08-20", "judge": "Hon. Justice Shetty"},
]

# ── 3. LEGAL AID PROVIDERS ────────────────────────────────────────────
legal_aid = [
    {"district": "Bengaluru Urban", "dlsa_name": "District Legal Services Authority, Bengaluru Urban", "address": "City Civil Court Complex, Upparpet, Bengaluru - 560002", "phone": "080-22971000", "helpline": "15100", "email": "dlsabengaluruurban@gmail.com", "secretary": "Adv. Ramya Krishnan", "services": ["Free legal advice", "Lok Adalat", "Bail assistance", "Women & child cases"], "timings": "Mon–Sat, 10:00 AM – 5:00 PM"},
    {"district": "Mysuru", "dlsa_name": "District Legal Services Authority, Mysuru", "address": "District Court Complex, Mysuru - 570024", "phone": "0821-2421100", "helpline": "15100", "email": "dlsamysuru@gmail.com", "secretary": "Adv. Shivakumar B.", "services": ["Free legal advice", "Lok Adalat", "Undertrial review", "Senior citizen cases"], "timings": "Mon–Sat, 10:00 AM – 5:00 PM"},
    {"district": "Dharwad", "dlsa_name": "District Legal Services Authority, Dharwad", "address": "District Court Complex, Dharwad - 580001", "phone": "0836-2447700", "helpline": "15100", "email": "dlsadharwad@gmail.com", "secretary": "Adv. Manjunath Kulkarni", "services": ["Free legal aid", "Lok Adalat", "Bail matters", "Land disputes"], "timings": "Mon–Sat, 10:00 AM – 5:00 PM"},
    {"district": "Dakshina Kannada", "dlsa_name": "District Legal Services Authority, Mangaluru", "address": "District Court Campus, Mangaluru - 575001", "phone": "0824-2421200", "helpline": "15100", "email": "dlsamangaluru@gmail.com", "secretary": "Adv. Latha Shetty", "services": ["Free legal advice", "Lok Adalat", "Maritime law", "Women & child protection"], "timings": "Mon–Sat, 10:00 AM – 5:00 PM"},
    {"district": "Kalaburagi", "dlsa_name": "District Legal Services Authority, Kalaburagi", "address": "District Court Complex, Kalaburagi - 585101", "phone": "08472-227700", "helpline": "15100", "email": "dlsakalaburagi@gmail.com", "secretary": "Adv. Basavaraj Patil", "services": ["Free legal advice", "Lok Adalat", "SC/ST protection", "Labour disputes"], "timings": "Mon–Sat, 10:00 AM – 5:00 PM"},
]

# ── 4. LEGAL PRECEDENTS ───────────────────────────────────────────────
precedents = [
    {"title": "D.K. Basu v. State of West Bengal", "year": 1997, "court": "Supreme Court of India", "citation": "AIR 1997 SC 610", "category": "Arrest & Detention", "ipc_sections": ["CrPC 41", "Article 21", "Article 22"], "summary": "Landmark judgment laying down guidelines for arrest and detention to prevent custodial torture. Established 11 mandatory requirements police must follow during arrest.", "key_principle": "No person can be subjected to torture or third degree treatment during arrest or detention.", "relevance": "high"},
    {"title": "Maneka Gandhi v. Union of India", "year": 1978, "court": "Supreme Court of India", "citation": "AIR 1978 SC 597", "category": "Fundamental Rights", "ipc_sections": ["Article 14", "Article 19", "Article 21"], "summary": "Expanded the interpretation of Article 21 (Right to Life) to include the right to live with dignity. Established that procedure must be fair, just, and reasonable.", "key_principle": "Right to life under Article 21 includes the right to live with dignity and cannot be curtailed by any unfair procedure.", "relevance": "high"},
    {"title": "Hussainara Khatoon v. State of Bihar", "year": 1979, "court": "Supreme Court of India", "citation": "AIR 1979 SC 1360", "category": "Bail & Undertrial Rights", "ipc_sections": ["Article 21", "CrPC 436A"], "summary": "Established the right to speedy trial as a fundamental right under Article 21. Led to release of thousands of undertrial prisoners who had spent more time in prison than their maximum sentence.", "key_principle": "An undertrial prisoner who has served the maximum sentence for the alleged offense must be released on bail.", "relevance": "high"},
    {"title": "State of Rajasthan v. Balchand", "year": 1977, "court": "Supreme Court of India", "citation": "AIR 1977 SC 2447", "category": "Bail & Undertrial Rights", "ipc_sections": ["CrPC 437", "CrPC 439", "Article 21"], "summary": "Established the principle that bail is the rule and jail is the exception for bailable offenses. Courts should lean towards granting bail unless there are compelling reasons.", "key_principle": "Bail is the rule, jail is the exception. Personal liberty is precious and courts should not deprive it lightly.", "relevance": "high"},
]

# ── Seed the database ─────────────────────────────────────────────────
def seed():
    print("Connecting to MongoDB Atlas...")
    
    # Test connection
    db.command("ping")
    print("Connected successfully!")

    # Clear existing data
    db.undertrials.delete_many({})
    db.hearings.delete_many({})
    db.legal_aid.delete_many({})
    db.precedents.delete_many({})
    print("Cleared existing collections")

    # Insert fresh data
    db.undertrials.insert_many(undertrials)
    print(f"Inserted {len(undertrials)} undertrials")

    db.hearings.insert_many(hearings)
    print(f"Inserted {len(hearings)} hearing records")

    db.legal_aid.insert_many(legal_aid)
    print(f"Inserted {len(legal_aid)} legal aid providers")

    db.precedents.insert_many(precedents)
    print(f"Inserted {len(precedents)} legal precedents")

    # Create indexes for fast search
    db.undertrials.create_index("prisoner_id", unique=True)
    db.undertrials.create_index("name")
    db.undertrials.create_index("district")
    db.hearings.create_index("prisoner_id")
    db.legal_aid.create_index("district")
    print("Created database indexes for fast search")

    print("\nDATABASE SETUP COMPLETE!")
    print(f"   Undertrials: {db.undertrials.count_documents({})}")
    print(f"   Hearings: {db.hearings.count_documents({})}")
    print(f"   Legal Aid: {db.legal_aid.count_documents({})}")
    print(f"   Precedents: {db.precedents.count_documents({})}")



if __name__ == "__main__":
    seed()
