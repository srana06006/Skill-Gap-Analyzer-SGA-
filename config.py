import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

class Config:
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")
    RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "jsearch.p.rapidapi.com")
    JSEARCH_URL = os.getenv("JSEARCH_URL", "https://jsearch.p.rapidapi.com/search")
    JSEARCH_FALLBACK = bool(int(os.getenv("JSEARCH_FALLBACK", "0")))

    ONET_API_USER = os.getenv("ONET_API_USER", "")
    ONET_API_PASS = os.getenv("ONET_API_PASS", "")
    ONET_BASE = os.getenv("ONET_BASE", "https://services.onetcenter.org/ws")

    DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "us")
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
