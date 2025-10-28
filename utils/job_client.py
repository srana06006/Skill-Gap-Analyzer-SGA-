from config import Config
def fetch_live_jobs(title, location, debug=False):
    # Fallback-only minimal stub so the app can render
    if Config.JSEARCH_FALLBACK or not Config.RAPIDAPI_KEY:
        return [
            {"title": f"{title} (Sample)", "company": "ExampleCorp",
             "desc": "Python, SQL, ML.", "link": "https://example.org/1", "location": location}
        ]
    return []
def get_last_error(): return None
