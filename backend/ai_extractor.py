from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

EXTRACTION_PROMPT = """
You are an expert at extracting structured information about opportunities (scholarships, fellowships, grants, accelerators, competitions, etc.) from web page text.

Extract the following fields from the text below. Return ONLY a valid JSON object, no extra text, no markdown, no backticks.

Fields to extract:
- title: name of the opportunity (string)
- organization: who is offering it (string)
- country: countries eligible or where it is based (string, comma separated)
- deadline: application deadline (string, e.g. "June 30, 2025" or "Rolling")
- eligibility: who can apply (string)
- funding_amount: money/stipend/grant amount if mentioned (string, e.g. "$10,000" or "Fully funded")
- category: type of opportunity (string, one of: Scholarship, Fellowship, Grant, Accelerator, Competition, Conference, Exchange, Government Scheme, Giveaway, Other)
- description: 2-3 sentence summary (string)
- tags: relevant tags (string, comma separated, e.g. "AI, Women, Startup, Research")
- is_remote: can it be done remotely (boolean)
- women_friendly: is it specifically for or friendly to women founders/applicants (boolean)
- indian_eligible: can Indian citizens/residents apply (boolean)
- student_eligible: is it open to students (boolean)
- age_min: minimum age requirement if mentioned (integer or null)
- age_max: maximum age requirement if mentioned (integer or null)
- application_fee: any fee to apply (string, e.g. "Free" or "$50")
- confidence: your confidence in this extraction from 0.0 to 1.0 (float)

Rules:
- If a field is not mentioned, use null for strings/integers, false for booleans
- For indian_eligible: true if open to all nationalities, or if India is explicitly mentioned
- For confidence: 0.9+ means all key fields found, 0.5-0.9 means partial info, below 0.5 means very little info

Return ONLY the JSON object. No explanation, no markdown, no backticks.

Text to extract from:
{text}
"""

def extract_opportunity(text: str, source_url: str = "") -> dict | None:
    try:
        truncated = text[:6000]
        prompt = EXTRACTION_PROMPT.format(text=truncated)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )

        raw = response.choices[0].message.content.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        data = json.loads(raw)
        data["source_url"] = source_url

        if data.get("confidence", 0) < 0.3:
            print(f"Low confidence ({data.get('confidence')}) for {source_url}")
            return None

        return data

    except json.JSONDecodeError as e:
        print(f"JSON parse error for {source_url}: {e}")
        return None
    except Exception as e:
        print(f"Extraction error for {source_url}: {e}")
        return None


def extract_batch(items: list[dict]) -> list[dict]:
    results = []
    for item in items:
        print(f"Extracting: {item.get('url', '')}")
        result = extract_opportunity(item.get("text", ""), item.get("url", ""))
        if result:
            results.append(result)
    return results