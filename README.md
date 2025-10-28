# 🧠 Skill-Gap Analyzer (SGA)

**Skill-Gap Analyzer (SGA)** is an AI-driven workforce analytics platform that pinpoints missing competencies in candidates or employees by analyzing three primary data sources — **résumés/CVs**, **job descriptions**, and **face-to-face interview performance**.  
It leverages **Natural Language Processing (NLP)** and **Machine Learning (ML)** to extract, match, and recommend the most efficient and affordable upskilling pathways.

---

## 🌟 Overview

Modern workplaces face a widening skill gap between what employers need and what candidates offer.  
SGA addresses this challenge by transforming unstructured data — from résumés, job postings, and interviews — into actionable insights.  
The platform not only highlights skill mismatches but also recommends personalized learning paths to bridge them.

---

## 🔍 Key Features

- **Automated Skill Extraction**  
  Uses NLP models (spaCy, TF-IDF) to parse résumés and job descriptions, identifying both explicit and implicit skills.

- **Competency Matching**  
  Quantifies alignment between a candidate’s skill profile and a job’s requirements using semantic similarity and machine learning.

- **Interview Performance Analytics**  
  Integrates facial, vocal, and textual cues (from recorded interviews) to assess communication clarity, confidence, and technical understanding.

- **Upskilling Recommendations**  
  Suggests micro-credentials, Coursera/edX courses, or targeted certifications to close the identified skill gaps.

- **Interactive Dashboard**  
  Visualizes gap trends, top missing skills, and personalized learning routes through dynamic charts and reports.

---

## 🧩 System Architecture


---

## 💻 Technology Stack

| Layer | Technologies |
|-------|---------------|
| **Backend** | Python (Flask API), Pandas, NumPy |
| **NLP/ML** | spaCy, scikit-learn, TF-IDF, Cosine Similarity |
| **Frontend** | HTML, JavaScript, Chart.js (Dashboard) |
| **Integration** | O*NET and LinkedIn APIs for real-time skill and occupation mapping |
| **Deployment** | Gunicorn + Flask (Cloud / Docker-ready) |

---

## 📊 Dashboard Features

- Displays **total candidate-job pairs analyzed**
- Shows **average missing skills per profile**
- Highlights **Top 10 skill gaps**
- Offers access to additional modules:
  - `/live-intelligence` → Real-time labor market trends  
  - `/skill-comparison` → Compare résumé vs. market skills  
  - `/career-coach` → Personalized course recommendations  
  - `/upskilling-pathway` → Visual learning progression

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
git clone https://github.com/srana06006/skill-gap-analyzer.git
cd skill-gap-analyzer

### 2️⃣ Create and Activate Virtual Environment
python -m venv venv
source venv/bin/activate     # on macOS/Linux
venv\Scripts\activate        # on Windows

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Set Up Environment Variables
Create a .env file in the root directory:

RAPIDAPI_KEY=your_rapidapi_key
ONET_API_USER=your_onet_username
ONET_API_PASS=your_onet_password

### 5️⃣ Run the Flask Application
export FLASK_APP=app.py
flask run

Access it at: http://127.0.0.1:5000/

---

## 🧠 Example Usage

**Step 1:** Upload or parse candidate résumés.  
**Step 2:** Match them against relevant job descriptions.  
**Step 3:** Visualize top missing skills and get recommended courses.  
**Step 4:** Use `/live-intelligence` for up-to-date market skill demand.




