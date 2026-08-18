import json

from app.adk.engine import StudioPilotEngine
from app.schemas.extraction.result import ExtractionResultV1
from app.services.pdf_service import PDFService


class DocumentExtractionService:

    def __init__(self, engine: StudioPilotEngine):
        self.engine = engine
        self.pdf_service = PDFService()

    def extract(self, document_path: str) -> ExtractionResultV1:

        text = self.pdf_service.extract_text(document_path)

        prompt = f"""
Analyze the following production document.

Extract the document metadata, scenes, characters, locations, and props.

Return ONLY valid JSON matching the required extraction structure.

Rules:

- Use only information present in the document.
- Never invent information.
- If information is unavailable, use an empty string, empty list, or null.
- Preserve names exactly where possible.
- Return JSON only.

DOCUMENT:

{text}
"""

        events = self.engine.run(
            user_id="document-extraction",
            text=prompt,
        )

        response_text = None

        for event in events:
            if event.is_final_response():
                response_text = event.content.parts[0].text
                break

        if not response_text:
            raise RuntimeError(
                "Document Agent returned no final response."
            )

        cleaned = response_text.strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```json", "", 1)
            cleaned = cleaned.replace("```", "", 1).strip()

        data = json.loads(cleaned)

        result = ExtractionResultV1.model_validate(data)

        return result