# 🌍 Opportunity Tracker

> AI-powered global opportunity discovery and tracking platform

An automated system that continuously discovers, categorizes, and tracks global opportunities — scholarships, fellowships, grants, accelerators, competitions, and more — for students, founders, researchers, and creators worldwide.

---

## ✨ Features

- 🤖 **AI Extraction Pipeline** — Uses Groq (Llama 3) to extract 16 structured fields from raw web pages
- 🔍 **Smart Search & Filters** — Search by keyword, category, country, eligibility
- 🇮🇳 **India-specific filters** — Dedicated Indian eligibility detection
- 👩 **Women-founder friendly** — Auto-detects women-focused opportunities
- 📅 **Auto-expiry** — Expired opportunities automatically archived
- 🔄 **Daily Automation** — GitHub Actions runs the scraper every day at 6 AM UTC
- 📊 **Application Tracker** — Track status: Saved → Applied → Interview → Accepted
- 🚀 **REST API** — Full FastAPI backend with auto-generated Swagger docs

---

## 🌐 Live Demo

- **Frontend:** https://opportunity-tracker-bay.vercel.app
- **Backend API:** https://opportunity-tracker-cmqw.onrender.com
- **API Documentation:** https://opportunity-tracker-cmqw.onrender.com/docs

---

## 🏗️ Architecture
Scraper (RSS + Web) → AI Extractor (Groq/Llama3) → SQLite DB → FastAPI → Next.js Dashboard

**Data flow:**
1. Scraper fetches raw HTML/text from opportunity sources daily
2. Groq AI extracts 16 structured fields with confidence scoring
3. Deduplication check before saving to database
4. FastAPI serves filtered data via REST endpoints
5. Next.js dashboard displays cards with search and filters

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15, React, Tailwind CSS |
| Backend | Python FastAPI, SQLAlchemy |
| Database | SQLite (local), PostgreSQL-ready |
| AI | Groq API (Llama 3.3 70B) |
| Scraping | BeautifulSoup4, Requests |
| Automation | GitHub Actions (daily cron) |
| Deployment | Vercel (frontend), Render (backend) |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Groq API key (free at console.groq.com)

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend` folder:
GROQ_API_KEY=your-groq-api-key-here

Run the backend:

```bash
uvicorn main:app --reload
```

API runs at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`

### Seed the database

```bash
python scraper.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Dashboard runs at `http://localhost:3000`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/opportunities` | List all opportunities with filters |
| GET | `/opportunities/{id}` | Get single opportunity |
| POST | `/track` | Track an application |
| GET | `/track` | Get all tracked applications |
| PUT | `/track/{id}` | Update tracking status |

### Filter Parameters
/opportunities?search=fellowship&category=Scholarship&indian_eligible=true&women_friendly=true&student_eligible=true

---

## 🤖 AI Extraction

The AI pipeline uses Groq Llama 3.3 70B to extract structured data from raw text.

**Extracted fields:** title, organization, country, deadline, eligibility, funding amount, category, description, tags, remote status, women-friendly flag, Indian eligibility, student eligibility, age limits, application fee, confidence score

**Confidence scoring:** Each extraction gets a 0.0–1.0 confidence score. Extractions below 0.3 are discarded automatically.

---

## ⚙️ Automation

GitHub Actions runs the scraper daily at 6 AM UTC:

```yaml
on:
  schedule:
    - cron: '0 6 * * *'
  workflow_dispatch:
```

---

## 📁 Project Structure
opportunity-tracker/
├── .github/
│   └── workflows/
│       └── daily_scraper.yml
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── scraper.py
│   ├── ai_extractor.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── app/
│       └── page.tsx
└── README.md

---

## 🎯 Roadmap

- [ ] Vector/semantic search using embeddings
- [ ] Email deadline reminders
- [ ] Telegram bot integration
- [ ] PostgreSQL production database
- [ ] More scraper sources (LinkedIn, govt portals)
- [ ] AI recommendation engine

---

Built with ❤️ for ambitious students, founders, and researchers worldwide.