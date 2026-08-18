from app.services.pdf_service import PDFService


pdf_path = "storage/documents/studiopilot_demo_movie_script.pdf"

text = PDFService().extract_text(pdf_path)

print("Characters:", len(text))
print()
print(text[:2000])