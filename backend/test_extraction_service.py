from app.adk.engine import StudioPilotEngine
from app.services.document_extraction_service import DocumentExtractionService


PDF_PATH = "storage/documents/knife.pdf"


engine = StudioPilotEngine()

service = DocumentExtractionService(engine)

result = service.extract(PDF_PATH)

print(result.model_dump_json(indent=2))