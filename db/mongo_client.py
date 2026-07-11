"""
MongoDB client — shared across all routes.
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "")

if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI not set in .env file")

client = MongoClient(MONGODB_URI)
db = client["nyaysetu"]

# Collections
undertrials_col = db["undertrials"]
hearings_col    = db["hearings"]
legal_aid_col   = db["legal_aid"]
precedents_col  = db["precedents"]
