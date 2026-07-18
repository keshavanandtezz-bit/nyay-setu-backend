"""
Nyay Setu - Database Seed Script
Clears and re-seeds all collections with comprehensive data.
Collections: undertrials, hearings, legal_aid, precedents, courts, cases
"""

import os
import certifi
from datetime import date, timedelta
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/nyay_setu")

# ---------------------------------------------------------------------------
# Connect
# ---------------------------------------------------------------------------
print("Connecting to MongoDB ...")
client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
db = client["nyaysetu"]
print(f"Connected -> database: {db.name}")

undertrials_col  = db["undertrials"]
hearings_col     = db["hearings"]
legal_aid_col    = db["legal_aid"]
precedents_col   = db["precedents"]
courts_col       = db["courts"]
cases_col        = db["cases"]

today = date.today()

def iso(d: date) -> str:
    return d.isoformat()


# ===========================================================================
# 1. UNDERTRIALS  (25 records)
# ===========================================================================
#  RED    (91-400 days) : P-1001,1002,1004,1007,1008,1009,1013,1014,1016,1018,1022,1023
#  YELLOW (61-90  days) : P-1005,1011,1020,1025,1020,1003 -> adjusted to 7 records
#  GREEN  (1-60   days) : remaining

raw_undertrials = [
    # --- RED (91-400 days) ---
    dict(prisoner_id="P-1001", name="Ramesh Kumar",       age=34, days=120,
         charges="Theft",             ipc_sections="379",
         court="Session Court Bengaluru",        district="Bengaluru Urban",
         has_lawyer=False, lawyer="",             prior_record=False,
         flight_risk="low",           offense_type="bailable",
         prison="Central Prison Bengaluru"),

    dict(prisoner_id="P-1002", name="Suresh Singh",       age=28, days=310,
         charges="Assault",           ipc_sections="323 324",
         court="District Court Mysuru",           district="Mysuru",
         has_lawyer=True,  lawyer="Adv. Priya Sharma", prior_record=True,
         flight_risk="medium",        offense_type="non-bailable",
         prison="District Prison Mysuru"),

    dict(prisoner_id="P-1004", name="Vijay Patel",        age=31, days=210,
         charges="Robbery",           ipc_sections="392",
         court="Session Court Hubballi",          district="Hubballi-Dharwad",
         has_lawyer=False, lawyer="",             prior_record=True,
         flight_risk="high",          offense_type="heinous",
         prison="Central Prison Hubballi"),

    dict(prisoner_id="P-1007", name="Sanjay Reddy",       age=29, days=95,
         charges="Domestic Violence", ipc_sections="498A 323",
         court="Session Court Bengaluru",         district="Bengaluru Urban",
         has_lawyer=False, lawyer="",             prior_record=False,
         flight_risk="medium",        offense_type="non-bailable",
         prison="Central Prison Bengaluru"),

    dict(prisoner_id="P-1008", name="Ravi Kumar",         age=52, days=380,
         charges="Murder",            ipc_sections="302",
         court="High Court Karnataka",            district="Shivamogga",
         has_lawyer=True,  lawyer="Adv. N. Hegde", prior_record=True,
         flight_risk="high",          offense_type="heinous",
         prison="Central Prison Shivamogga"),

    dict(prisoner_id="P-1009", name="Pradeep Naik",       age=24, days=130,
         charges="Attempt to Murder", ipc_sections="307",
         court="Session Court Tumkuru",           district="Tumkuru",
         has_lawyer=False, lawyer="",             prior_record=False,
         flight_risk="medium",        offense_type="heinous",
         prison="District Prison Tumkuru"),

    dict(prisoner_id="P-1013", name="Basavaraja Gowda",   age=55, days=200,
         charges="Dowry Death",       ipc_sections="304B",
         court="Session Court Bengaluru Rural",   district="Bengaluru Rural",
         has_lawyer=True,  lawyer="Adv. M. Rao", prior_record=False,
         flight_risk="low",           offense_type="heinous",
         prison="Central Prison Bengaluru"),

    dict(prisoner_id="P-1014", name="Shankar Rao",        age=36, days=145,
         charges="Rape",              ipc_sections="376",
         court="Session Court Mysuru",            district="Mysuru",
         has_lawyer=False, lawyer="",             prior_record=True,
         flight_risk="high",          offense_type="heinous",
         prison="District Prison Mysuru"),

    # --- YELLOW (61-90 days) ---
    dict(prisoner_id="P-1003", name="Arun Sharma",        age=45, days=75,
         charges="Fraud",             ipc_sections="420 468",
         court="District Court Mangaluru",        district="Mangaluru",
         has_lawyer=True,  lawyer="Adv. K. Nair", prior_record=False,
         flight_risk="low",           offense_type="bailable",
         prison="District Prison Mangaluru"),

    dict(prisoner_id="P-1005", name="Deepak Verma",       age=22, days=70,
         charges="Property Dispute",  ipc_sections="447",
         court="District Court Belagavi",         district="Belagavi",
         has_lawyer=False, lawyer="",             prior_record=False,
         flight_risk="low",           offense_type="minor",
         prison="District Prison Belagavi"),

    dict(prisoner_id="P-1011", name="Gururaj Patil",      age=33, days=80,
         charges="Grievous Hurt",     ipc_sections="326",
         court="District Court Ballari",          district="Ballari",
         has_lawyer=False, lawyer="",             prior_record=False,
         flight_risk="medium",        offense_type="non-bailable",
         prison="District Prison Ballari"),

    dict(prisoner_id="P-1016", name="Farooq Ahmed",       age=44, days=260,
         charges="Dacoity",           ipc_sections="395",
         court="Session Court Mangaluru",         district="Mangaluru",
         has_lawyer=True,  lawyer="Adv. R. Alvares", prior_record=True,
         flight_risk="high",          offense_type="heinous",
         prison="District Prison Mangaluru"),

    dict(prisoner_id="P-1018", name="Venkatesh Rao",      age=39, days=110,
         charges="Cheating",          ipc_sections="420 406",
         court="District Court Belagavi",         district="Belagavi",
         has_lawyer=False, lawyer="",             prior_record=False,
         flight_risk="medium",        offense_type="non-bailable",
         prison="District Prison Belagavi"),

    dict(prisoner_id="P-1020", name="Prakash Nayak",      age=48, days=65,
         charges="Domestic Violence", ipc_sections="498A 406",
         court="District Court Shivamogga",       district="Shivamogga",
         has_lawyer=True,  lawyer="Adv. G. Hegde", prior_record=False,
         flight_risk="medium",        offense_type="non-bailable",
         prison="District Prison Shivamogga"),

    dict(prisoner_id="P-1025", name="Mallikarjun S.",     age=23, days=88,
         charges="Attempt to Murder", ipc_sections="307",
         court="Session Court Bengaluru",         district="Bengaluru Urban",
         has_lawyer=False, lawyer="",             prior_record=False,
         flight_risk="medium",        offense_type="heinous",
         prison="Central Prison Bengaluru"),

    # --- GREEN (1-60 days) ---
    dict(prisoner_id="P-1006", name="Mohammed Imran",     age=38, days=15,
         charges="Cheating",          ipc_sections="420",
         court="JMFC Court Kalaburagi",           district="Kalaburagi",
         has_lawyer=True,  lawyer="Adv. B. Desai", prior_record=False,
         flight_risk="low",           offense_type="bailable",
         prison="District Prison Kalaburagi"),

    dict(prisoner_id="P-1010", name="Anwar Khan",         age=41, days=55,
         charges="Forgery",           ipc_sections="468 471",
         court="District Court Vijayapura",       district="Vijayapura",
         has_lawyer=True,  lawyer="Adv. S. Patil", prior_record=False,
         flight_risk="low",           offense_type="bailable",
         prison="District Prison Vijayapura"),

    dict(prisoner_id="P-1012", name="Krishnamurthy",      age=47, days=35,
         charges="House-breaking",    ipc_sections="454",
         court="JMFC Court Raichur",              district="Raichur",
         has_lawyer=False, lawyer="",             prior_record=False,
         flight_risk="low",           offense_type="bailable",
         prison="District Prison Raichur"),

    dict(prisoner_id="P-1015", name="Manjunath Swamy",    age=27, days=20,
         charges="Theft",             ipc_sections="379 380",
         court="JMFC Bengaluru",                  district="Bengaluru Urban",
         has_lawyer=False, lawyer="",             prior_record=False,
         flight_risk="low",           offense_type="bailable",
         prison="Central Prison Bengaluru"),

    dict(prisoner_id="P-1017", name="Nagaraju P.",        age=30, days=25,
         charges="Assault",           ipc_sections="323",
         court="JMFC Hubballi",                   district="Hubballi-Dharwad",
         has_lawyer=False, lawyer="",             prior_record=False,
         flight_risk="low",           offense_type="minor",
         prison="District Prison Hubballi"),

    dict(prisoner_id="P-1019", name="Sunil Kumar",        age=26, days=8,
         charges="Theft",             ipc_sections="379",
         court="JMFC Kalaburagi",                 district="Kalaburagi",
         has_lawyer=False, lawyer="",             prior_record=False,
         flight_risk="low",           offense_type="bailable",
         prison="District Prison Kalaburagi"),

    dict(prisoner_id="P-1021", name="Abdul Rehman",       age=35, days=48,
         charges="Fraud",             ipc_sections="420",
         court="District Court Tumkuru",          district="Tumkuru",
         has_lawyer=False, lawyer="",             prior_record=False,
         flight_risk="low",           offense_type="bailable",
         prison="District Prison Tumkuru"),

    dict(prisoner_id="P-1022", name="Shivananda K.",      age=42, days=320,
         charges="Murder",            ipc_sections="302",
         court="Session Court Vijayapura",        district="Vijayapura",
         has_lawyer=True,  lawyer="Adv. H. Joshi", prior_record=True,
         flight_risk="high",          offense_type="heinous",
         prison="District Prison Vijayapura"),

    dict(prisoner_id="P-1023", name="Rajesh Tiwari",      age=31, days=170,
         charges="Robbery",           ipc_sections="392 394",
         court="Session Court Ballari",           district="Ballari",
         has_lawyer=False, lawyer="",             prior_record=False,
         flight_risk="high",          offense_type="heinous",
         prison="District Prison Ballari"),

    dict(prisoner_id="P-1024", name="Hanumantha Reddy",   age=58, days=30,
         charges="Property Dispute",  ipc_sections="447 427",
         court="District Court Raichur",          district="Raichur",
         has_lawyer=True,  lawyer="Adv. Y. Singh", prior_record=False,
         flight_risk="low",           offense_type="minor",
         prison="District Prison Raichur"),
]

undertrials_docs = []
for r in raw_undertrials:
    days = r.pop("days")
    arrest_dt = today - timedelta(days=days)
    next_h_dt = today + timedelta(days=14)
    r["arrest_date"]    = iso(arrest_dt)
    r["next_hearing"]   = iso(next_h_dt)
    r["case_status"]    = "Under Trial"
    r["days_in_custody"] = days
    undertrials_docs.append(r)

try:
    undertrials_col.delete_many({})
    res = undertrials_col.insert_many(undertrials_docs)
    print(f"[OK] Undertrials  : inserted {len(res.inserted_ids)} records")
except Exception as e:
    print(f"[ERROR] Undertrials  : {e}")


# ===========================================================================
# 2. HEARINGS  (46 records)
# ===========================================================================

def hearing(pid, date_offset, outcome, judge, next_date_offset=None):
    h_date = today - timedelta(days=date_offset)
    court_name = next((u["court"] for u in undertrials_docs if u["prisoner_id"] == pid), "")
    doc = dict(
        prisoner_id=pid,
        hearing_date=iso(h_date),
        outcome=outcome,
        judge=judge,
        court_name=court_name,
        notes=f"Hearing on {iso(h_date)} — {outcome}"
    )
    if next_date_offset is not None:
        doc["next_hearing_date"] = iso(today + timedelta(days=next_date_offset))
    return doc

hearings_docs = [
    # P-1001 (120 days, Theft, Bengaluru)
    hearing("P-1001", 110, "Chargesheet Filed",  "Hon. Justice B.N. Rao", 90),
    hearing("P-1001",  80, "Bail Rejected",       "Hon. Justice B.N. Rao", 50),
    hearing("P-1001",  20, "Adjourned",           "Hon. Justice B.N. Rao", 14),

    # P-1002 (310 days, Assault, Mysuru)
    hearing("P-1002", 300, "Chargesheet Filed",  "Hon. Justice S.R. Krishna", 260),
    hearing("P-1002", 250, "Bail Rejected",       "Hon. Justice S.R. Krishna", 200),
    hearing("P-1002", 180, "Cross-examination",   "Hon. Justice S.R. Krishna", 140),
    hearing("P-1002",  60, "Arguments Heard",     "Hon. Justice S.R. Krishna",  21),

    # P-1004 (210 days, Robbery, Hubballi)
    hearing("P-1004", 200, "Chargesheet Filed",  "Hon. Justice R.V. Patil", 160),
    hearing("P-1004", 140, "Bail Rejected",       "Hon. Justice R.V. Patil", 100),
    hearing("P-1004",  50, "Evidence Submitted",  "Hon. Justice R.V. Patil",  20),

    # P-1007 (95 days, Domestic Violence, Bengaluru)
    hearing("P-1007",  88, "Bail Rejected",       "Hon. Justice K. Suresh",   60),
    hearing("P-1007",  45, "Adjourned",           "Hon. Justice K. Suresh",   30),
    hearing("P-1007",  10, "Cross-examination",   "Hon. Justice K. Suresh",   14),

    # P-1008 (380 days, Murder, Shivamogga)
    hearing("P-1008", 370, "Chargesheet Filed",  "Hon. Justice N.V. Anjaria", 330),
    hearing("P-1008", 300, "Bail Rejected",       "Hon. Justice N.V. Anjaria", 260),
    hearing("P-1008", 210, "Evidence Submitted",  "Hon. Justice N.V. Anjaria", 170),
    hearing("P-1008", 120, "Cross-examination",   "Hon. Justice N.V. Anjaria",  80),
    hearing("P-1008",  30, "Arguments Heard",     "Hon. Justice N.V. Anjaria",  21),

    # P-1009 (130 days, Attempt to Murder, Tumkuru)
    hearing("P-1009", 120, "Chargesheet Filed",  "Hon. Justice T.G. Naik",   90),
    hearing("P-1009",  70, "Bail Rejected",       "Hon. Justice T.G. Naik",   40),
    hearing("P-1009",  15, "Evidence Submitted",  "Hon. Justice T.G. Naik",   14),

    # P-1011 (80 days, Grievous Hurt, Ballari)
    hearing("P-1011",  75, "Bail Rejected",       "Hon. Justice P.R. Hegde",  45),
    hearing("P-1011",  35, "Adjourned",           "Hon. Justice P.R. Hegde",  21),
    hearing("P-1011",   7, "Chargesheet Filed",   "Hon. Justice P.R. Hegde",  14),

    # P-1013 (200 days, Dowry Death, Bengaluru Rural)
    hearing("P-1013", 190, "Chargesheet Filed",  "Hon. Justice D.L. Rao",   155),
    hearing("P-1013", 130, "Bail Rejected",       "Hon. Justice D.L. Rao",    90),
    hearing("P-1013",  65, "Cross-examination",   "Hon. Justice D.L. Rao",    30),
    hearing("P-1013",  10, "Evidence Submitted",  "Hon. Justice D.L. Rao",    14),

    # P-1014 (145 days, Rape, Mysuru)
    hearing("P-1014", 138, "Chargesheet Filed",  "Hon. Justice A.S. Bopanna", 110),
    hearing("P-1014",  90, "Bail Rejected",       "Hon. Justice A.S. Bopanna",  60),
    hearing("P-1014",  25, "Cross-examination",   "Hon. Justice A.S. Bopanna",  21),

    # P-1016 (260 days, Dacoity, Mangaluru)
    hearing("P-1016", 250, "Chargesheet Filed",  "Hon. Justice C.V. Alvares", 210),
    hearing("P-1016", 180, "Bail Rejected",       "Hon. Justice C.V. Alvares", 140),
    hearing("P-1016", 100, "Evidence Submitted",  "Hon. Justice C.V. Alvares",  60),
    hearing("P-1016",  20, "Arguments Heard",     "Hon. Justice C.V. Alvares",  14),

    # P-1018 (110 days, Cheating, Belagavi)
    hearing("P-1018", 100, "Chargesheet Filed",  "Hon. Justice M.G. Kumari",  70),
    hearing("P-1018",  55, "Bail Rejected",       "Hon. Justice M.G. Kumari",  30),
    hearing("P-1018",  12, "Adjourned",           "Hon. Justice M.G. Kumari",  21),

    # P-1022 (320 days, Murder, Vijayapura)
    hearing("P-1022", 310, "Chargesheet Filed",  "Hon. Justice F.R. Joshi",  270),
    hearing("P-1022", 240, "Bail Rejected",       "Hon. Justice F.R. Joshi",  200),
    hearing("P-1022", 160, "Cross-examination",   "Hon. Justice F.R. Joshi",  120),
    hearing("P-1022",  70, "Evidence Submitted",  "Hon. Justice F.R. Joshi",   30),
    hearing("P-1022",   8, "Arguments Heard",     "Hon. Justice F.R. Joshi",   21),

    # P-1023 (170 days, Robbery, Ballari)
    hearing("P-1023", 165, "Chargesheet Filed",  "Hon. Justice G.V. Reddy",  130),
    hearing("P-1023", 100, "Bail Rejected",       "Hon. Justice G.V. Reddy",   65),
    hearing("P-1023",  30, "Evidence Submitted",  "Hon. Justice G.V. Reddy",   14),

    # P-1025 (88 days, Attempt to Murder, Bengaluru)
    hearing("P-1025",  82, "Bail Rejected",       "Hon. Justice B.K. Nair",   55),
    hearing("P-1025",  40, "Chargesheet Filed",   "Hon. Justice B.K. Nair",   25),
    hearing("P-1025",   5, "Adjourned",           "Hon. Justice B.K. Nair",   14),
]

try:
    hearings_col.delete_many({})
    res = hearings_col.insert_many(hearings_docs)
    print(f"[OK] Hearings     : inserted {len(res.inserted_ids)} records")
except Exception as e:
    print(f"[ERROR] Hearings     : {e}")


# ===========================================================================
# 3. LEGAL AID  (15 records)
# ===========================================================================

legal_aid_docs = [
    dict(name="Karnataka State Legal Services Authority (KSLSA)",
         district="Bengaluru Urban", phone="1800-425-9090",
         email="kslsa@karnataka.gov.in",
         address="Nyaya Degula, H.Siddaiah Road, Bengaluru",
         specialization="General Criminal, Civil Rights",
         availability="Mon-Sat 10AM-5PM", type="Government"),

    dict(name="Bengaluru Urban District Legal Services Authority (DLSA)",
         district="Bengaluru Urban", phone="080-22867890",
         email="dlsa.blr@karnataka.gov.in",
         address="City Civil Court Complex, Bengaluru",
         specialization="Bail, Undertrial Rights",
         availability="Mon-Fri 10AM-5PM", type="Government"),

    dict(name="Mysuru DLSA",
         district="Mysuru", phone="0821-2330130",
         email="dlsa.mysuru@karnataka.gov.in",
         address="District Court Complex, Mysuru",
         specialization="Criminal Defense, Civil",
         availability="Mon-Fri 10AM-5PM", type="Government"),

    dict(name="Mangaluru DLSA",
         district="Mangaluru", phone="0824-2422234",
         email="dlsa.mng@karnataka.gov.in",
         address="Court Hill, Mangaluru",
         specialization="Domestic Violence, Labor",
         availability="Mon-Fri 10AM-4PM", type="Government"),

    dict(name="Hubballi-Dharwad DLSA",
         district="Hubballi-Dharwad", phone="0836-2224567",
         email="dlsa.hbd@karnataka.gov.in",
         address="Court Complex, Hubballi",
         specialization="Bail, Criminal",
         availability="Mon-Sat 9AM-5PM", type="Government"),

    dict(name="Belagavi DLSA",
         district="Belagavi", phone="0831-2401234",
         email="dlsa.blg@karnataka.gov.in",
         address="District Court, Belagavi",
         specialization="Criminal, Civil",
         availability="Mon-Fri 10AM-4PM", type="Government"),

    dict(name="Kalaburagi DLSA",
         district="Kalaburagi", phone="08472-224455",
         email="dlsa.klb@karnataka.gov.in",
         address="Court Complex, Kalaburagi",
         specialization="Criminal, Rural Rights",
         availability="Mon-Fri 10AM-4PM", type="Government"),

    dict(name="Shivamogga DLSA",
         district="Shivamogga", phone="08182-222344",
         email="dlsa.smg@karnataka.gov.in",
         address="District Court, Shivamogga",
         specialization="Criminal, Civil",
         availability="Mon-Fri 9AM-5PM", type="Government"),

    dict(name="SICHREM - Society for Integrated Coastal Management",
         district="Bengaluru Urban", phone="080-25498843",
         email="sichrem@gmail.com",
         address="14 Richmond Road, Bengaluru",
         specialization="Human Rights, Prison Reform",
         availability="Mon-Fri 9AM-6PM", type="NGO"),

    dict(name="Human Rights Law Network (HRLN)",
         district="Bengaluru Urban", phone="080-41214592",
         email="hrln.bangalore@gmail.com",
         address="Lavelle Road, Bengaluru",
         specialization="Constitutional Rights, Undertrial",
         availability="Mon-Fri 10AM-5PM", type="NGO"),

    dict(name="Tumkuru DLSA",
         district="Tumkuru", phone="0816-2255678",
         email="dlsa.tmk@karnataka.gov.in",
         address="District Court, Tumkuru",
         specialization="Criminal, Civil",
         availability="Mon-Fri 10AM-4PM", type="Government"),

    dict(name="Vijayapura DLSA",
         district="Vijayapura", phone="08352-255123",
         email="dlsa.vjp@karnataka.gov.in",
         address="Court Complex, Vijayapura",
         specialization="Criminal, Civil",
         availability="Mon-Fri 10AM-4PM", type="Government"),

    dict(name="Ballari DLSA",
         district="Ballari", phone="08392-235678",
         email="dlsa.bll@karnataka.gov.in",
         address="District Court, Ballari",
         specialization="Criminal, Mining Rights",
         availability="Mon-Fri 10AM-5PM", type="Government"),

    dict(name="Raichur DLSA",
         district="Raichur", phone="08532-228901",
         email="dlsa.rch@karnataka.gov.in",
         address="District Court, Raichur",
         specialization="Criminal, Civil",
         availability="Mon-Fri 10AM-4PM", type="Government"),

    dict(name="Praaja (People's Union for Civil Liberties)",
         district="Bengaluru Urban", phone="080-22867777",
         email="pucl.karnataka@gmail.com",
         address="Gandhi Nagar, Bengaluru",
         specialization="Civil Liberties, Undertrial Rights",
         availability="Mon-Sat 10AM-6PM", type="NGO"),
]

try:
    legal_aid_col.delete_many({})
    res = legal_aid_col.insert_many(legal_aid_docs)
    print(f"[OK] Legal Aid    : inserted {len(res.inserted_ids)} records")
except Exception as e:
    print(f"[ERROR] Legal Aid    : {e}")


# ===========================================================================
# 4. LEGAL PRECEDENTS  (25 records)
# ===========================================================================

precedents_docs = [
    dict(title="Hussainara Khatoon vs Home Secretary Bihar",
         case_number="1979 AIR 1360", court="Supreme Court of India",
         date="1979-03-09",
         summary=("The Supreme Court held that the right to a speedy trial is a fundamental "
                  "right enshrined under Article 21 of the Constitution. The Court directed "
                  "the release of undertrial prisoners who had been in custody for periods "
                  "exceeding the maximum sentence for their alleged offence."),
         ipc_sections="General", category="Undertrial Rights",
         outcome="Right to Speedy Trial Affirmed"),

    dict(title="Arnesh Kumar vs State of Bihar",
         case_number="Crl.A.1277/2014", court="Supreme Court of India",
         date="2014-07-02",
         summary=("The Supreme Court issued comprehensive guidelines restraining police from "
                  "automatically arresting accused persons under Section 498A IPC. Magistrates "
                  "were directed to apply their mind independently before authorising detention. "
                  "A checklist mechanism was mandated for all such cases."),
         ipc_sections="498A", category="Arrest Guidelines",
         outcome="Arrest Guidelines Issued"),

    dict(title="D.K. Basu vs State of West Bengal",
         case_number="1997 1 SCC 416", court="Supreme Court of India",
         date="1996-12-18",
         summary=("The Supreme Court laid down eleven binding requirements that must be followed "
                  "in all cases of arrest and detention to safeguard the rights of the accused. "
                  "These guidelines cover identification of arresting officers, health check-ups, "
                  "intimation of family, and maintenance of arrest memos."),
         ipc_sections="General", category="Human Rights",
         outcome="Arrest Procedures Mandated"),

    dict(title="Maneka Gandhi vs Union of India",
         case_number="1978 AIR 597", court="Supreme Court of India",
         date="1978-01-25",
         summary=("A seven-judge bench expanded the scope of Article 21, holding that the right "
                  "to life and personal liberty cannot be curtailed except by a procedure that is "
                  "fair, just, and reasonable. This landmark judgment gave a broad and purposive "
                  "interpretation to fundamental rights."),
         ipc_sections="General", category="Constitutional Law",
         outcome="Expanded Article 21"),

    dict(title="Prem Shankar Shukla vs Delhi Administration",
         case_number="1980 3 SCC 526", court="Supreme Court of India",
         date="1980-08-21",
         summary=("The Supreme Court declared the practice of handcuffing undertrial prisoners "
                  "unconstitutional as it violates Articles 14, 19, and 21 of the Constitution. "
                  "Handcuffing is permissible only in extraordinary circumstances with prior "
                  "judicial permission."),
         ipc_sections="General", category="Prisoner Rights",
         outcome="Handcuffing Restricted"),

    dict(title="Sunil Batra vs Delhi Administration",
         case_number="1978 4 SCC 494", court="Supreme Court of India",
         date="1978-11-06",
         summary=("The Court held that solitary confinement of prisoners is a punitive "
                  "measure and cannot be imposed without proper judicial scrutiny. Prison "
                  "authorities must follow due process before imposing harsh conditions on "
                  "prisoners, and habeas corpus may be used to challenge such conditions."),
         ipc_sections="General", category="Prisoner Rights",
         outcome="Solitary Confinement Restricted"),

    dict(title="Sheela Barse vs State of Maharashtra",
         case_number="1983 2 SCC 96", court="Supreme Court of India",
         date="1983-02-15",
         summary=("The Supreme Court addressed the plight of women prisoners in Maharashtra "
                  "jails and issued directions for their protection. The Court mandated free "
                  "legal aid for women prisoners and directed that they be kept in separate "
                  "cells with female guards."),
         ipc_sections="General", category="Prisoner Rights",
         outcome="Women Prisoner Rights"),

    dict(title="Francis Coralie Mullin vs Administrator UT Delhi",
         case_number="1981 1 SCC 608", court="Supreme Court of India",
         date="1981-01-13",
         summary=("The Court held that the right to live with basic human dignity, free from "
                  "exploitation, is implicit in Article 21. Pre-trial detention must not be "
                  "punitive and the right to a speedy trial is an integral part of the right "
                  "to life under the Constitution."),
         ipc_sections="General", category="Constitutional Law",
         outcome="Right to Dignity"),

    dict(title="State vs Balchand Jain",
         case_number="1977 4 SCC 308", court="Supreme Court of India",
         date="1977-10-07",
         summary=("The Supreme Court clarified the provisions relating to bail in default under "
                  "Section 437 CrPC and held that where an undertrial has been in custody beyond "
                  "the prescribed period, bail cannot be ordinarily refused. Courts must actively "
                  "consider bail applications of long-incarcerated undertrials."),
         ipc_sections="General", category="Bail Rights",
         outcome="Bail Default Provision"),

    dict(title="Moti Ram vs State of Madhya Pradesh",
         case_number="1978 4 SCC 47", court="Supreme Court of India",
         date="1978-10-07",
         summary=("The Court liberalised bail surety conditions and held that imposing excessive "
                  "sureties effectively denies bail to poor accused persons. Courts must consider "
                  "the economic capacity of the accused and allow personal bonds where sureties "
                  "cannot be furnished."),
         ipc_sections="General", category="Bail Rights",
         outcome="Surety Relaxation"),

    dict(title="Sanjay Chandra vs CBI",
         case_number="2012 1 SCC 40", court="Supreme Court of India",
         date="2011-11-23",
         summary=("In the 2G spectrum case, the Supreme Court granted bail to the accused "
                  "holding that bail is the rule and jail the exception. The Court held that "
                  "Article 21 guarantees the right to liberty even in economic offences unless "
                  "compelling reasons exist to deny bail."),
         ipc_sections="420", category="Bail Rights",
         outcome="Bail Granted Economic Offence"),

    dict(title="Satender Kumar Antil vs CBI",
         case_number="2022 10 SCC 51", court="Supreme Court of India",
         date="2022-07-11",
         summary=("The Supreme Court issued comprehensive guidelines on default bail under "
                  "Section 167(2) CrPC and directed trial courts to ensure that undertrials "
                  "who have completed half their maximum sentence are considered for release. "
                  "The Court also directed establishment of undertrial review committees."),
         ipc_sections="General", category="Bail Rights",
         outcome="Default Bail Guidelines"),

    dict(title="Arnesh Kumar Judgment Clarification",
         case_number="2014 8 SCC 273", court="Supreme Court of India",
         date="2014-07-02",
         summary=("Supplementing the primary Arnesh Kumar judgment, the Court issued a mandatory "
                  "checklist that magistrates must use before authorising detention in Section "
                  "498A and 406 IPC cases. The Court held that mechanical authorisation of "
                  "detention without application of mind is unconstitutional."),
         ipc_sections="498A 406", category="Arrest Guidelines",
         outcome="Mandatory Checklist"),

    dict(title="Joginder Kumar vs State of Uttar Pradesh",
         case_number="1994 4 SCC 260", court="Supreme Court of India",
         date="1994-04-25",
         summary=("The Supreme Court held that police must justify the need to arrest and that "
                  "arrest cannot be made merely because it is lawful. Justification for arrest "
                  "must be recorded and the arrested person must be informed of grounds of "
                  "arrest in accordance with Article 22."),
         ipc_sections="General", category="Arrest Guidelines",
         outcome="Justification Required"),

    dict(title="Nilabati Behera vs State of Orissa",
         case_number="1993 2 SCC 746", court="Supreme Court of India",
         date="1993-03-24",
         summary=("The Court awarded monetary compensation for custodial death holding that "
                  "the State is liable for violation of fundamental rights of persons in its "
                  "custody. Public law compensation under Article 32 or 226 is distinct from "
                  "private law remedies and can be awarded directly by constitutional courts."),
         ipc_sections="General", category="Human Rights",
         outcome="State Liability Custodial Death"),

    dict(title="Rudul Sah vs State of Bihar",
         case_number="1983 4 SCC 141", court="Supreme Court of India",
         date="1983-08-01",
         summary=("The Court awarded monetary compensation to a person who was illegally "
                  "detained for over 14 years after his acquittal. This was the first case "
                  "where the Supreme Court directly awarded compensation for violation of "
                  "fundamental rights under Article 21."),
         ipc_sections="General", category="Human Rights",
         outcome="Compensation for Illegal Detention"),

    dict(title="Re: Inhuman Conditions in 1382 Prisons",
         case_number="WP Crl 406/2013", court="Supreme Court of India",
         date="2016-02-05",
         summary=("Taking suo motu cognisance of prison conditions across India, the Supreme "
                  "Court issued directions to reduce overcrowding, improve healthcare, provide "
                  "legal aid, and address the mental health needs of prisoners. The judgment "
                  "set timelines for state governments to implement systemic prison reforms."),
         ipc_sections="General", category="Prison Reform",
         outcome="Reform Directives"),

    dict(title="Thana Singh vs Central Bureau of Narcotics",
         case_number="2013 2 SCC 590", court="Supreme Court of India",
         date="2013-01-30",
         summary=("The Court held that default bail under Section 167(2) CrPC applies to NDPS "
                  "cases as well and that the absence of prosecution sanction does not bar the "
                  "grant of default bail. The accused's right to default bail is an indefeasible "
                  "right that cannot be defeated by delayed sanction."),
         ipc_sections="General", category="Bail Rights",
         outcome="Default Bail NDPS"),

    dict(title="Nikesh Tarachand Shah vs Union of India",
         case_number="2018 11 SCC 1", court="Supreme Court of India",
         date="2017-11-23",
         summary=("The Supreme Court struck down the twin conditions for bail under the PMLA "
                  "as unconstitutional. The Court held that the conditions placed an unreasonable "
                  "burden on the accused and violated Articles 14 and 21 of the Constitution."),
         ipc_sections="General", category="Bail Rights",
         outcome="PMLA Bail Conditions"),

    dict(title="Gurucharan Singh vs State Delhi Administration",
         case_number="1978 1 SCC 118", court="Supreme Court of India",
         date="1978-02-24",
         summary=("The Supreme Court enumerated the factors to be considered by courts while "
                  "deciding bail applications under Sections 437 and 439 CrPC. These include "
                  "the nature of accusation, severity of punishment, character, means, and "
                  "the antecedents of the accused."),
         ipc_sections="General", category="Bail Rights",
         outcome="Bail Factors Enumerated"),

    dict(title="State of Karnataka vs Krishappa",
         case_number="2021 KHC 4231", court="Karnataka High Court",
         date="2021-06-12",
         summary=("The Karnataka High Court clarified the conditions under which bail pending "
                  "appeal after conviction may be granted. The Court held that gravity of "
                  "offence, likelihood of success in appeal, and period already undergone are "
                  "the primary considerations."),
         ipc_sections="302", category="Bail Rights",
         outcome="Bail Pending Appeal"),

    dict(title="Rehman Shagoo vs State of J&K",
         case_number="2018 SC 897", court="Supreme Court of India",
         date="2018-03-14",
         summary=("The Court clarified the conditions and limitations on anticipatory bail "
                  "under Section 438 CrPC and held that anticipatory bail cannot be granted "
                  "for an indefinite period without conditions. Courts must impose appropriate "
                  "conditions to balance liberty with investigation requirements."),
         ipc_sections="General", category="Bail Rights",
         outcome="Anticipatory Bail Conditions"),

    dict(title="Geeta Mehrotra vs State of Uttar Pradesh",
         case_number="2012 10 SCC 741", court="Supreme Court of India",
         date="2012-01-07",
         summary=("The Supreme Court held that distant relatives named in a Section 498A FIR "
                  "cannot be automatically arrested without specific allegations against them. "
                  "The Court emphasised that FIR contents must disclose specific roles before "
                  "arrest of all named persons is authorised."),
         ipc_sections="498A", category="Arrest Guidelines",
         outcome="Relatives Protection"),

    dict(title="Imtiyaz Ahmed vs State of Uttar Pradesh",
         case_number="2012 2 SCC 688", court="Supreme Court of India",
         date="2012-01-18",
         summary=("The Court issued a comprehensive set of directions to subordinate courts "
                  "to ensure speedy disposal of cases within prescribed timelines. The judgment "
                  "mandated day-to-day trial in serious criminal cases and directed high courts "
                  "to monitor compliance through quarterly reports."),
         ipc_sections="General", category="Undertrial Rights",
         outcome="Trial Timeline Directives"),

    dict(title="In Re: Policy Strategy for Grant of Bail",
         case_number="WP 88/2019", court="Supreme Court of India",
         date="2022-09-14",
         summary=("The Supreme Court reaffirmed the 'bail not jail' policy and directed all "
                  "courts to consider bail liberally so as to reduce prison overcrowding. The "
                  "Court observed that excessive undertrial detention violates Article 21 and "
                  "directed states to establish bail clinics and undertrial review committees."),
         ipc_sections="General", category="Bail Rights",
         outcome="Bail Not Jail Policy"),
]

try:
    precedents_col.delete_many({})
    res = precedents_col.insert_many(precedents_docs)
    print(f"[OK] Precedents   : inserted {len(res.inserted_ids)} records")
except Exception as e:
    print(f"[ERROR] Precedents   : {e}")


# ===========================================================================
# 5. COURTS  (30 records)
# ===========================================================================

courts_docs = [
    # Bengaluru Urban (11)
    dict(name="Karnataka High Court",
         court_type="High Court", district="Bengaluru Urban",
         address="High Court Buildings, Dr. D.V. Sadananda Gowda Rd, Bengaluru 560001",
         phone="080-22868021", judge="Hon. Chief Justice P.S. Dinesh Kumar",
         established=1884, cases_pending=45320, timings="Mon-Fri 10:30AM-4:30PM"),

    dict(name="Session Court Bengaluru (Principal)",
         court_type="Sessions Court", district="Bengaluru Urban",
         address="City Civil Court Complex, Sampige Rd, Bengaluru 560001",
         phone="080-22867800", judge="Hon. Principal District & Sessions Judge V.K. Mohan",
         established=1974, cases_pending=12450, timings="Mon-Sat 10AM-5PM"),

    dict(name="Session Court Bengaluru (Fast Track - II)",
         court_type="Sessions Court", district="Bengaluru Urban",
         address="City Civil Court Complex, Sampige Rd, Bengaluru 560001",
         phone="080-22867850", judge="Hon. Additional Sessions Judge R. Divya",
         established=2002, cases_pending=4380, timings="Mon-Sat 10AM-5PM"),

    dict(name="District Court Bengaluru",
         court_type="District Court", district="Bengaluru Urban",
         address="City Civil Court Complex, Sampige Rd, Bengaluru 560001",
         phone="080-22867900", judge="Hon. District Judge S. Narayan",
         established=1960, cases_pending=9870, timings="Mon-Sat 10AM-5PM"),

    dict(name="JMFC Court Bengaluru - I",
         court_type="JMFC", district="Bengaluru Urban",
         address="JMFC Court Complex, Avenue Road, Bengaluru 560002",
         phone="080-22351200", judge="Hon. JMFC A. Sumalatha",
         established=1980, cases_pending=6540, timings="Mon-Sat 10AM-5PM"),

    dict(name="JMFC Court Bengaluru - IV",
         court_type="JMFC", district="Bengaluru Urban",
         address="JMFC Court Complex, Avenue Road, Bengaluru 560002",
         phone="080-22351240", judge="Hon. JMFC D. Krishnamurthy",
         established=1985, cases_pending=5210, timings="Mon-Sat 10AM-5PM"),

    dict(name="Family Court Bengaluru",
         court_type="Family Court", district="Bengaluru Urban",
         address="Hosur Road, Near Madivala, Bengaluru 560068",
         phone="080-25561234", judge="Hon. Principal Judge (Family) M. Lalitha",
         established=1996, cases_pending=3870, timings="Mon-Sat 10AM-5PM"),

    dict(name="Fast Track Court Bengaluru (POCSO / Women)",
         court_type="Fast Track Court", district="Bengaluru Urban",
         address="City Civil Court Complex, Sampige Rd, Bengaluru 560001",
         phone="080-22867870", judge="Hon. Special Judge (POCSO) S. Geetha",
         established=2013, cases_pending=1980, timings="Mon-Sat 10AM-5PM"),

    dict(name="Lok Adalat Bengaluru (City Civil)",
         court_type="Lok Adalat", district="Bengaluru Urban",
         address="City Civil Court Complex, Sampige Rd, Bengaluru 560001",
         phone="080-22867911", judge="Panel of Mediators",
         established=1988, cases_pending=0, timings="Sat 10AM-4PM"),

    dict(name="Lok Adalat Bengaluru (Motor Accident)",
         court_type="Lok Adalat", district="Bengaluru Urban",
         address="High Court Annexe, Bengaluru 560001",
         phone="080-22868050", judge="Panel of Mediators (MACT)",
         established=1995, cases_pending=0, timings="Sat 10AM-4PM"),

    dict(name="Lok Adalat Bengaluru (Banking & Cheque)",
         court_type="Lok Adalat", district="Bengaluru Urban",
         address="Magadi Road Court Complex, Bengaluru 560023",
         phone="080-23373456", judge="Panel of Mediators (Banking)",
         established=2000, cases_pending=0, timings="Last Sat of Month 10AM-4PM"),

    # Mysuru (3)
    dict(name="Session Court Mysuru",
         court_type="Sessions Court", district="Mysuru",
         address="Court Road, Mysuru 570001",
         phone="0821-2330456", judge="Hon. Principal Sessions Judge B.V. Prakash",
         established=1970, cases_pending=5640, timings="Mon-Sat 10AM-5PM"),

    dict(name="District Court Mysuru",
         court_type="District Court", district="Mysuru",
         address="Court Road, Mysuru 570001",
         phone="0821-2330400", judge="Hon. District Judge N. Usha",
         established=1968, cases_pending=4210, timings="Mon-Sat 10AM-5PM"),

    dict(name="JMFC Court Mysuru",
         court_type="JMFC", district="Mysuru",
         address="JMFC Complex, Nazarbad, Mysuru 570010",
         phone="0821-2440230", judge="Hon. JMFC K. Venugopal",
         established=1978, cases_pending=3380, timings="Mon-Sat 10AM-5PM"),

    # Mangaluru (2)
    dict(name="Session Court Mangaluru",
         court_type="Sessions Court", district="Mangaluru",
         address="Court Hill Road, Mangaluru 575001",
         phone="0824-2422200", judge="Hon. Sessions Judge C.V. D'Silva",
         established=1972, cases_pending=4120, timings="Mon-Sat 10AM-5PM"),

    dict(name="District Court Mangaluru",
         court_type="District Court", district="Mangaluru",
         address="Court Hill Road, Mangaluru 575001",
         phone="0824-2422210", judge="Hon. District Judge R.M. Alvares",
         established=1968, cases_pending=3760, timings="Mon-Sat 10AM-5PM"),

    # Hubballi-Dharwad (2)
    dict(name="Session Court Hubballi",
         court_type="Sessions Court", district="Hubballi-Dharwad",
         address="Court Area, Hubballi 580020",
         phone="0836-2224100", judge="Hon. Principal Sessions Judge P.G. Kulkarni",
         established=1975, cases_pending=4870, timings="Mon-Sat 10AM-5PM"),

    dict(name="District Court Dharwad",
         court_type="District Court", district="Hubballi-Dharwad",
         address="Circuit House Road, Dharwad 580001",
         phone="0836-2447800", judge="Hon. District Judge S.M. Patil",
         established=1965, cases_pending=3920, timings="Mon-Sat 10AM-5PM"),

    # Belagavi (2)
    dict(name="Session Court Belagavi",
         court_type="Sessions Court", district="Belagavi",
         address="Tilakwadi Court Complex, Belagavi 590006",
         phone="0831-2401100", judge="Hon. Principal Sessions Judge A.K. Jadhav",
         established=1968, cases_pending=5230, timings="Mon-Sat 10AM-5PM"),

    dict(name="District Court Belagavi",
         court_type="District Court", district="Belagavi",
         address="Tilakwadi Court Complex, Belagavi 590006",
         phone="0831-2401200", judge="Hon. District Judge V. Mirji",
         established=1966, cases_pending=4100, timings="Mon-Sat 10AM-5PM"),

    # Kalaburagi (1)
    dict(name="Session Court Kalaburagi",
         court_type="Sessions Court", district="Kalaburagi",
         address="Court Circle, Kalaburagi 585101",
         phone="08472-224300", judge="Hon. Sessions Judge B.N. Desai",
         established=1978, cases_pending=3640, timings="Mon-Sat 10AM-5PM"),

    # Shivamogga (1)
    dict(name="Session Court Shivamogga",
         court_type="Sessions Court", district="Shivamogga",
         address="Court Area, Shivamogga 577201",
         phone="08182-222100", judge="Hon. Sessions Judge G.S. Hegde",
         established=1977, cases_pending=3290, timings="Mon-Sat 10AM-5PM"),

    # Tumkuru (2)
    dict(name="Session Court Tumkuru",
         court_type="Sessions Court", district="Tumkuru",
         address="Court Road, Tumkuru 572101",
         phone="0816-2255100", judge="Hon. Sessions Judge H.N. Naik",
         established=1980, cases_pending=2980, timings="Mon-Sat 10AM-5PM"),

    dict(name="District Court Tumkuru",
         court_type="District Court", district="Tumkuru",
         address="Court Road, Tumkuru 572101",
         phone="0816-2255200", judge="Hon. District Judge P.N. Kumar",
         established=1977, cases_pending=2650, timings="Mon-Sat 10AM-5PM"),

    # Vijayapura (2)
    dict(name="Session Court Vijayapura",
         court_type="Sessions Court", district="Vijayapura",
         address="Court Road, Vijayapura 586101",
         phone="08352-255000", judge="Hon. Sessions Judge F.A. Joshi",
         established=1978, cases_pending=2750, timings="Mon-Sat 10AM-5PM"),

    dict(name="District Court Vijayapura",
         court_type="District Court", district="Vijayapura",
         address="Court Road, Vijayapura 586101",
         phone="08352-255100", judge="Hon. District Judge S.R. Patil",
         established=1975, cases_pending=2320, timings="Mon-Sat 10AM-5PM"),

    # Ballari (1)
    dict(name="Session Court Ballari",
         court_type="Sessions Court", district="Ballari",
         address="Court Complex, Ballari 583101",
         phone="08392-235100", judge="Hon. Sessions Judge G.V. Reddy",
         established=1976, cases_pending=3150, timings="Mon-Sat 10AM-5PM"),

    # Raichur (2)
    dict(name="Session Court Raichur",
         court_type="Sessions Court", district="Raichur",
         address="Court Road, Raichur 584101",
         phone="08532-228700", judge="Hon. Sessions Judge Y.B. Singh",
         established=1975, cases_pending=2890, timings="Mon-Sat 10AM-5PM"),

    dict(name="District Court Raichur",
         court_type="District Court", district="Raichur",
         address="Court Road, Raichur 584101",
         phone="08532-228800", judge="Hon. District Judge K.V. Reddy",
         established=1974, cases_pending=2100, timings="Mon-Sat 10AM-5PM"),

    # Bengaluru Rural (1)
    dict(name="Session Court Bengaluru Rural",
         court_type="Sessions Court", district="Bengaluru Rural",
         address="Devanahalli Road, Bengaluru Rural 562110",
         phone="080-27671234", judge="Hon. Sessions Judge M.R. Krishnaiah",
         established=1990, cases_pending=2140, timings="Mon-Sat 10AM-5PM"),
]

try:
    courts_col.delete_many({})
    res = courts_col.insert_many(courts_docs)
    print(f"[OK] Courts       : inserted {len(res.inserted_ids)} records")
except Exception as e:
    print(f"[ERROR] Courts       : {e}")


# ===========================================================================
# 6. CASES  (10 records)
# ===========================================================================
# 3 trial | 2 chargesheet | 3 investigation | 2 fir_filed

def make_case(case_id, complainant, phone, district, category, description,
              stage, days_since_filed, stage_history, police_station):
    filed_at     = today - timedelta(days=days_since_filed)
    last_updated = today - timedelta(days=1)
    return dict(
        case_id=case_id,
        complainant_name=complainant,
        phone=phone,
        district=district,
        category=category,
        description=description,
        stage=stage,
        filed_at=iso(filed_at),
        last_updated=iso(last_updated),
        stage_history=stage_history,
        police_station=police_station,
        documents=[],
    )

cases_docs = [
    # --- TRIAL (3) ---
    make_case("CS-10001", "Savitha R.", "9880123456", "Bengaluru Urban",
              "Domestic Violence",
              "Complainant reports repeated physical and emotional abuse by husband over 3 years.",
              "trial", 320,
              [
                  {"stage": "registered",    "date": iso(today - timedelta(days=320)), "note": "Complaint registered"},
                  {"stage": "fir_filed",     "date": iso(today - timedelta(days=315)), "note": "FIR filed at HSR Layout PS"},
                  {"stage": "investigation", "date": iso(today - timedelta(days=280)), "note": "Medical examination done"},
                  {"stage": "chargesheet",   "date": iso(today - timedelta(days=200)), "note": "Chargesheet filed u/s 498A 323"},
                  {"stage": "trial",         "date": iso(today - timedelta(days=150)), "note": "Trial commenced at Session Court"},
              ],
              "HSR Layout Police Station"),

    make_case("CS-10002", "Narayana Swamy", "7760987654", "Mysuru",
              "Fraud",
              "Complainant alleges financial fraud of Rs.12 lakhs by a real estate agent promising plots.",
              "trial", 280,
              [
                  {"stage": "registered",    "date": iso(today - timedelta(days=280)), "note": "Complaint registered at Lakshmipuram PS"},
                  {"stage": "fir_filed",     "date": iso(today - timedelta(days=275)), "note": "FIR filed u/s 420"},
                  {"stage": "investigation", "date": iso(today - timedelta(days=240)), "note": "Bank statements seized"},
                  {"stage": "chargesheet",   "date": iso(today - timedelta(days=170)), "note": "Chargesheet filed"},
                  {"stage": "trial",         "date": iso(today - timedelta(days=120)), "note": "Trial commenced"},
              ],
              "Lakshmipuram Police Station"),

    make_case("CS-10003", "Meera Devi", "8970345678", "Belagavi",
              "Theft",
              "Jewellery worth Rs.3.5 lakhs stolen from residence during daytime in absence of family.",
              "trial", 200,
              [
                  {"stage": "registered",    "date": iso(today - timedelta(days=200)), "note": "Complaint registered"},
                  {"stage": "fir_filed",     "date": iso(today - timedelta(days=196)), "note": "FIR filed u/s 379"},
                  {"stage": "investigation", "date": iso(today - timedelta(days=170)), "note": "CCTV footage collected"},
                  {"stage": "chargesheet",   "date": iso(today - timedelta(days=110)), "note": "Chargesheet filed"},
                  {"stage": "trial",         "date": iso(today - timedelta(days=60)),  "note": "Trial commenced"},
              ],
              "Belagavi City Police Station"),

    # --- CHARGESHEET (2) ---
    make_case("CS-10004", "Venkat Prasad", "9741234567", "Mangaluru",
              "Assault",
              "Complainant assaulted by neighbour during property boundary dispute causing grievous injuries.",
              "chargesheet", 160,
              [
                  {"stage": "registered",    "date": iso(today - timedelta(days=160)), "note": "Complaint registered"},
                  {"stage": "fir_filed",     "date": iso(today - timedelta(days=157)), "note": "FIR filed u/s 323 325"},
                  {"stage": "investigation", "date": iso(today - timedelta(days=120)), "note": "Witnesses recorded"},
                  {"stage": "chargesheet",   "date": iso(today - timedelta(days=30)),  "note": "Chargesheet filed with court"},
              ],
              "Kadri Police Station"),

    make_case("CS-10005", "Roopa Shetty", "9632587410", "Hubballi-Dharwad",
              "Cyber Crime",
              "Complainant fell victim to online banking fraud. Rs.85,000 debited via OTP phishing.",
              "chargesheet", 130,
              [
                  {"stage": "registered",    "date": iso(today - timedelta(days=130)), "note": "Online complaint registered"},
                  {"stage": "fir_filed",     "date": iso(today - timedelta(days=126)), "note": "FIR filed u/s 66C IT Act"},
                  {"stage": "investigation", "date": iso(today - timedelta(days=90)),  "note": "IP address traced"},
                  {"stage": "chargesheet",   "date": iso(today - timedelta(days=20)),  "note": "Chargesheet filed"},
              ],
              "Cyber Crime Police Station Hubballi"),

    # --- INVESTIGATION (3) ---
    make_case("CS-10006", "Prakash Gowda", "9876054321", "Shivamogga",
              "Property Dispute",
              "Encroachment of agricultural land (2 acres) by neighbour backed by forged sale deed.",
              "investigation", 90,
              [
                  {"stage": "registered",    "date": iso(today - timedelta(days=90)), "note": "Complaint registered at Shivamogga Rural PS"},
                  {"stage": "fir_filed",     "date": iso(today - timedelta(days=85)), "note": "FIR filed u/s 447 468"},
                  {"stage": "investigation", "date": iso(today - timedelta(days=60)), "note": "Revenue records seized for verification"},
              ],
              "Shivamogga Rural Police Station"),

    make_case("CS-10007", "Lakshmi Bai", "9535678901", "Kalaburagi",
              "Domestic Violence",
              "Married woman reports repeated violence and harassment for dowry by in-laws.",
              "investigation", 75,
              [
                  {"stage": "registered",    "date": iso(today - timedelta(days=75)), "note": "Complaint at Women's PS"},
                  {"stage": "fir_filed",     "date": iso(today - timedelta(days=72)), "note": "FIR filed u/s 498A 406"},
                  {"stage": "investigation", "date": iso(today - timedelta(days=55)), "note": "Accused called for questioning"},
              ],
              "Women Police Station Kalaburagi"),

    make_case("CS-10008", "Mohammed Yusuf", "9448523690", "Tumkuru",
              "Fraud",
              "Complainant cheated by fake job placement agency; paid Rs.1.8 lakh and not placed.",
              "investigation", 50,
              [
                  {"stage": "registered",    "date": iso(today - timedelta(days=50)), "note": "Complaint registered"},
                  {"stage": "fir_filed",     "date": iso(today - timedelta(days=47)), "note": "FIR filed u/s 420"},
                  {"stage": "investigation", "date": iso(today - timedelta(days=35)), "note": "Agent's office raided, documents seized"},
              ],
              "Tumkuru Town Police Station"),

    # --- FIR FILED (2) ---
    make_case("CS-10009", "Suresh Babu", "9341267890", "Vijayapura",
              "Theft",
              "Two-wheeler stolen from government hospital parking area in broad daylight.",
              "fir_filed", 20,
              [
                  {"stage": "registered",    "date": iso(today - timedelta(days=20)), "note": "Complaint registered at Vijayapura City PS"},
                  {"stage": "fir_filed",     "date": iso(today - timedelta(days=18)), "note": "FIR filed u/s 379"},
              ],
              "Vijayapura City Police Station"),

    make_case("CS-10010", "Anitha Kumari", "8971230456", "Ballari",
              "Cyber Crime",
              "Fake Instagram account created using complainant's photos; used for extortion.",
              "fir_filed", 12,
              [
                  {"stage": "registered",    "date": iso(today - timedelta(days=12)), "note": "Complaint at Cyber PS Ballari"},
                  {"stage": "fir_filed",     "date": iso(today - timedelta(days=10)), "note": "FIR filed u/s 66C 66D IT Act"},
              ],
              "Cyber Crime Police Station Ballari"),
]

try:
    cases_col.delete_many({})
    res = cases_col.insert_many(cases_docs)
    print(f"[OK] Cases        : inserted {len(res.inserted_ids)} records")
except Exception as e:
    print(f"[ERROR] Cases        : {e}")


# ===========================================================================
# 7. INDEXES
# ===========================================================================
print("\nCreating indexes ...")

try:
    undertrials_col.create_index("prisoner_id", unique=True)
    undertrials_col.create_index("name")
    undertrials_col.create_index("district")
    print("[OK] Undertrials indexes created")
except Exception as e:
    print(f"[ERROR] Undertrials index: {e}")

try:
    hearings_col.create_index("prisoner_id")
    hearings_col.create_index("hearing_date")
    print("[OK] Hearings indexes created")
except Exception as e:
    print(f"[ERROR] Hearings index: {e}")

try:
    cases_col.create_index("case_id", unique=True)
    cases_col.create_index("phone")
    print("[OK] Cases indexes created")
except Exception as e:
    print(f"[ERROR] Cases index: {e}")

try:
    courts_col.create_index("district")
    courts_col.create_index("court_type")
    print("[OK] Courts indexes created")
except Exception as e:
    print(f"[ERROR] Courts index: {e}")

try:
    legal_aid_col.create_index("district")
    print("[OK] Legal Aid indexes created")
except Exception as e:
    print(f"[ERROR] Legal Aid index: {e}")

try:
    precedents_col.create_index("category")
    print("[OK] Precedents indexes created")
except Exception as e:
    print(f"[ERROR] Precedents index: {e}")


# ===========================================================================
# 8. SUMMARY
# ===========================================================================
print("\n" + "=" * 55)
print("  SEED COMPLETE - Collection Counts")
print("=" * 55)
print(f"  undertrials  : {undertrials_col.count_documents({})}")
print(f"  hearings     : {hearings_col.count_documents({})}")
print(f"  legal_aid    : {legal_aid_col.count_documents({})}")
print(f"  precedents   : {precedents_col.count_documents({})}")
print(f"  courts       : {courts_col.count_documents({})}")
print(f"  cases        : {cases_col.count_documents({})}")
print("=" * 55)

client.close()
print("Connection closed. Seeding finished successfully.")
