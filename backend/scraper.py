import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from database import SessionLocal, create_tables
from models import Opportunity
from ai_extractor import extract_opportunity
import hashlib
import time

def get_url_hash(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()

def is_duplicate(db, url: str) -> bool:
    existing = db.query(Opportunity).filter(Opportunity.link == url).first()
    return existing is not None

def save_opportunity(db, data: dict) -> bool:
    try:
        if is_duplicate(db, data.get("link") or data.get("source_url", "")):
            print(f"Duplicate skipped: {data.get('title')}")
            return False

        opp = Opportunity(
            title=data.get("title", "Untitled")[:500],
            organization=data.get("organization", "")[:300] if data.get("organization") else None,
            country=data.get("country", "")[:200] if data.get("country") else None,
            deadline=data.get("deadline", "")[:100] if data.get("deadline") else None,
            eligibility=data.get("eligibility"),
            funding_amount=data.get("funding_amount", "")[:200] if data.get("funding_amount") else None,
            category=data.get("category", "Other")[:100],
            link=data.get("link") or data.get("source_url", ""),
            description=data.get("description"),
            tags=data.get("tags", "")[:500] if data.get("tags") else None,
            is_remote=data.get("is_remote", False),
            women_friendly=data.get("women_friendly", False),
            indian_eligible=data.get("indian_eligible", False),
            student_eligible=data.get("student_eligible", False),
            age_min=data.get("age_min"),
            age_max=data.get("age_max"),
            application_fee=data.get("application_fee", "")[:100] if data.get("application_fee") else None,
            source_url=data.get("source_url", ""),
            is_active=True,
        )
        db.add(opp)
        db.commit()
        print(f"Saved: {opp.title}")
        return True
    except Exception as e:
        db.rollback()
        print(f"Save error: {e}")
        return False

def scrape_opportunity_desk():
    print("Scraping Opportunity Desk RSS...")
    results = []
    try:
        rss_url = "https://opportunitydesk.org/feed/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(rss_url, headers=headers, timeout=15)
        root = ET.fromstring(response.content)

        items = root.findall(".//item")[:10]
        for item in items:
            title = item.findtext("title", "")
            link = item.findtext("link", "")
            description = item.findtext("description", "")
            content = f"{title}\n{description}"
            results.append({"text": content, "url": link})
        print(f"Found {len(results)} items from Opportunity Desk")
    except Exception as e:
        print(f"Opportunity Desk scrape error: {e}")
    return results

def scrape_youth_opportunities():
    print("Scraping Youth Opportunities...")
    results = []
    try:
        url = "https://youthop.com/scholarships"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")

        cards = soup.find_all("article")[:8]
        for card in cards:
            title_el = card.find(["h2", "h3", "h4"])
            link_el = card.find("a", href=True)
            desc_el = card.find("p")

            title = title_el.get_text(strip=True) if title_el else ""
            link = link_el["href"] if link_el else ""
            desc = desc_el.get_text(strip=True) if desc_el else ""

            if title and link:
                if not link.startswith("http"):
                    link = "https://youthop.com" + link
                results.append({"text": f"{title}\n{desc}", "url": link})

        print(f"Found {len(results)} items from Youth Opportunities")
    except Exception as e:
        print(f"Youth Opportunities scrape error: {e}")
    return results

def scrape_sample_opportunities():
    print("Loading sample opportunities...")
    samples = [
        {
            "text": """Google Summer of Code 2025 - Open Source Internship Program
Google Summer of Code is a global program focused on bringing more developers into open source software development.
Students work with an open source organization on a 3 month programming project.
Stipend: $1500-$6600 USD. Open to students 18+ worldwide including India.
Deadline: April 2025. Free to apply. Remote program.""",
            "url": "https://summerofcode.withgoogle.com"
        },
        {
            "text": """Chevening Scholarships 2025-2026 - UK Government
Chevening is the UK government's international awards programme. Fully funded masters scholarships.
Open to professionals with 2 years work experience from eligible countries including India.
Covers tuition, living expenses, flights. Deadline: November 2025. Free application.""",
            "url": "https://www.chevening.org/scholarships/"
        },
        {
            "text": """YCombinator W25 Startup Accelerator
Y Combinator provides seed funding and mentorship for early stage startups.
$500,000 investment for 7% equity. 3 month program in San Francisco.
Open to startup founders worldwide. Women founders encouraged to apply.
Deadline: Rolling admissions. No application fee.""",
            "url": "https://www.ycombinator.com/apply"
        },
        {
            "text": """Fulbright Foreign Student Program 2025
The Fulbright Program is the US government's flagship international educational exchange program.
Fully funded grants for graduate study, research, or teaching in the United States.
Open to students and young professionals from India and 160+ countries.
Deadline: October 2025. Free to apply.""",
            "url": "https://foreign.fulbrightonline.org"
        },
        {
            "text": """Microsoft for Startups Founders Hub - Cloud Credits Giveaway
Microsoft for Startups provides up to $150,000 in Azure cloud credits plus GitHub, Microsoft 365.
Open to early stage startups worldwide including India. Women founders welcome.
No equity taken. Free to apply. Rolling admissions.""",
            "url": "https://foundershub.startups.microsoft.com"
        },
        {
            "text": """UN Women Youth Leadership Program 2025
United Nations program for young women leaders aged 18-30.
Fully funded fellowship including travel, accommodation and stipend.
Focus on gender equality and women empowerment. Open to women from developing countries including India.
Deadline: August 2025.""",
            "url": "https://www.unwomen.org/fellowships"
        },
        {
            "text": """AWS Activate for Startups - Free Cloud Credits
Amazon Web Services offers up to $100,000 in AWS credits for early stage startups.
Also includes technical support, training, and access to AWS experts.
Open to startups worldwide including India. Free to apply. Rolling admissions.""",
            "url": "https://aws.amazon.com/activate"
        },
        {
            "text": """DAAD Scholarships Germany 2025 - Research Grants for India
German Academic Exchange Service scholarships for Indian students and researchers.
Fully funded research stays at German universities for 1-6 months.
Open to Indian graduates and doctoral candidates. Monthly stipend 1200 EUR.
Deadline: November 2025. Free application.""",
            "url": "https://www.daad.in/en/find-funding/scholarships-for-indians/"
        },
    ]
    return samples

def run_scraper():
    print("Starting scraper...")
    create_tables()
    db = SessionLocal()
    total_saved = 0

    try:
        all_items = []
        all_items.extend(scrape_sample_opportunities())
        all_items.extend(scrape_opportunity_desk())
        all_items.extend(scrape_youth_opportunities())

        print(f"\nTotal items to process: {len(all_items)}")
        print("Running AI extraction...\n")

        for item in all_items:
            extracted = extract_opportunity(item["text"], item["url"])
            if extracted:
                extracted["link"] = item["url"]
                if save_opportunity(db, extracted):
                    total_saved += 1
            time.sleep(1)

        print(f"\nScraper done! Saved {total_saved} new opportunities.")
    finally:
        db.close()

if __name__ == "__main__":
    run_scraper()