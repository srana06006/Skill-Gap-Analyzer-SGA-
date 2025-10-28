import os, json, re, logging
from pathlib import Path
from collections import Counter
from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
from dotenv import load_dotenv

from utils.onet_client import search_occupation, get_skills_for_occupation
from utils.job_client import fetch_live_jobs, get_last_error
from utils.skill_extractor import extract_skills
from utils.course_recommender import coursera_courses

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["JSON_SORT_KEYS"] = False
logging.basicConfig(level=logging.INFO)

@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/live-intelligence")
def live_intelligence_page():
    return render_template("live_intelligence.html")

@app.route("/skill-comparison")
def skill_comparison_page():
    return render_template("skill_comparison.html")

@app.route("/career-coach")
def career_coach_page():
    return render_template("career_coach.html")

@app.route("/upskilling-pathway")
def upskilling_pathway_page():
    return render_template("upskilling_pathway.html")

@app.route("/api/dashboard")
def dashboard_data():
    path = BASE_DIR / "dataset" / "skill_gap_dataset.csv"
    if not path.exists():
        return jsonify({"error": "dataset/skill_gap_dataset.csv not found",
                        "num_records": 0, "avg_missing": 0, "top_missing": []})
    df = pd.read_csv(path)

    def parse_list(x):
        if isinstance(x, list):
            return x
        if isinstance(x, str) and x.strip().startswith("["):
            try:
                return json.loads(x)
            except Exception:
                return []
        return []

    if "missing_skills" in df.columns:
        df["missing_skills"] = df["missing_skills"].apply(parse_list)
    else:
        df["missing_skills"] = [[] for _ in range(len(df))]

    df["missing_count"] = df["missing_skills"].apply(len)
    all_missing = [s for lst in df["missing_skills"] for s in lst]
    top = Counter(all_missing).most_common(10)

    return jsonify({
        "num_records": int(len(df)),
        "avg_missing": round(float(df["missing_count"].mean()) if len(df) else 0.0, 2),
        "top_missing": [{"skill": s, "count": int(c)} for s, c in top]
    })

@app.route("/api/live_intelligence")
def live_intelligence_api():
    title = request.args.get("title", "Data Scientist")
    location = request.args.get("loc", "United States")

    jobs = fetch_live_jobs(title, location)
    onet_skills = []
    occs = search_occupation(title)
    if occs:
        onet_skills = get_skills_for_occupation(occs[0]["code"])

    all_text = " ".join([(j.get("desc") or "") for j in jobs]).lower()
    from collections import Counter as C
    freq = C()
    for s in onet_skills:
        nm = (s.get("name") or "").lower()
        if nm:
            freq[nm] = all_text.count(nm)
    top = [{"skill": s, "count": int(c)} for s, c in freq.most_common(15)]

    return jsonify({
        "query": title,
        "total_jobs": len(jobs),
        "top_skill_freq": top,
        "jobs": jobs,
        "debug_error": get_last_error()
    })

@app.route("/api/skill_comparison", methods=["POST"])
def skill_comparison():
    data = request.get_json(force=True)
    resume = data.get("resume", "")
    title = data.get("title", "Data Scientist")
    location = data.get("loc", "United States")

    cand_skills = set(re.findall(r"[a-zA-Z0-9\+\#\.]{3,}", resume.lower()))

    occs = search_occupation(title)
    onet = [s["name"].lower() for s in get_skills_for_occupation(occs[0]["code"])] if occs else []
    jobs = fetch_live_jobs(title, location)
    market_text = " ".join([j.get("desc", "") for j in jobs]).lower()
    market_tokens = set(re.findall(r"[a-zA-Z0-9\+\#\.]{3,}", market_text))

    overlap = sorted(cand_skills & set(onet))
    missing = sorted(set(onet) - cand_skills)
    emerging = sorted(market_tokens - set(onet))

    return jsonify({
        "overlap": overlap[:40],
        "missing": missing[:40],
        "emerging": emerging[:40],
        "stats": {
            "overlap_pct": round(len(overlap) / len(onet) * 100, 2) if onet else 0.0
        }
    })

@app.route("/api/recommend_courses", methods=["POST"])
def recommend_courses():
    data = request.get_json(force=True)
    resume = data.get("resume", "")
    missing = data.get("missing", [])

    extracted = extract_skills(resume)
    recs = []
    for s in missing[:10]:
        for c in coursera_courses(s, limit=1):
            recs.append({"skill": s, **c})

    return jsonify({
        "extracted_skills": extracted,
        "course_recommendations": recs
    })

@app.route("/api/upskilling_pathway", methods=["POST"])
def upskilling_pathway():
    data = request.get_json(force=True)
    missing = data.get("missing", [])
    pathway = []
    total = 0

    for s in missing[:5]:
        cs = coursera_courses(s, limit=1)
        if not cs:
            continue
        c = cs[0]
        dur_raw = str(c.get("duration", "10"))
        nums = re.findall(r"\d+", dur_raw)
        hours = int(nums[0]) if nums else 10
        total += hours
        entry = dict(c)
        entry["skill"] = s
        entry["duration"] = hours
        pathway.append(entry)

    return jsonify({
        "pathway": pathway,
        "total_duration_hours": total,
        "estimated_weeks": round(total / 10.0, 1)
    })

@app.route("/api/debug_env")
def debug_env():
    import os
    return jsonify({
        "HAS_RAPIDAPI_KEY": bool(os.getenv("RAPIDAPI_KEY")),
        "HAS_ONET_API_USER": bool(os.getenv("ONET_API_USER")),
        "HAS_ONET_API_PASS": bool(os.getenv("ONET_API_PASS")),
        "JSEARCH_FALLBACK": bool(int(os.getenv("JSEARCH_FALLBACK", "0")))
    })

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(app.static_folder, "favicon.ico", mimetype="image/x-icon")

if __name__ == "__main__":
    app.run(debug=True)
