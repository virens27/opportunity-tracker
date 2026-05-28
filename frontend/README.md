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

## 🏗️ Architecture