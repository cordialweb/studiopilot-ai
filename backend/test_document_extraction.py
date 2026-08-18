import json

from app.services.pdf_service import PDFService
from app.adk.engine import StudioPilotEngine
from app.schemas.extraction.result import ExtractionResultV1


PDF_PATH = "storage/documents/knife.pdf"


pdf_service = PDFService()
engine = StudioPilotEngine()

text = pdf_service.extract_text(PDF_PATH)

print(f"Extracted characters: {len(text)}")

prompt = f"""
Analyze the following production document.

Extract the document metadata, scenes, characters, locations, and props.

Return ONLY valid JSON matching this structure:

{{
  "document": {{
    "title": "",
    "author": "",
    "genre": "",
    "language": "",
    "pages": 0,
    "summary": ""
  }},
  "scenes": [],
  "characters": [],
  "locations": [],
  "props": []
}}

Rules:

- Use only information present in the document.
- Never invent information.
- If information is unavailable, use an empty string, empty list, or null.
- Preserve names exactly where possible.
- Return JSON only.

DOCUMENT:

{text}
"""

events = engine.run(
    user_id="document-test",
    text=prompt,
)

response_text = None

for event in events:
    if event.is_final_response():
        response_text = event.content.parts[0].text
        break

if not response_text:
    raise RuntimeError("No final response received from DocumentAgent.")

print("\n--- RAW GEMINI RESPONSE ---\n")
print(response_text)

cleaned = response_text.strip()

if cleaned.startswith("```"):
    cleaned = cleaned.replace("```json", "", 1)
    cleaned = cleaned.replace("```", "", 1).strip()

data = json.loads(cleaned)

result = ExtractionResultV1.model_validate(data)

print("\n--- VALIDATED EXTRACTION ---\n")
print(result.model_dump_json(indent=2))