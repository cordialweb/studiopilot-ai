import pymupdf


class PDFService:

    def extract_text(self, filepath: str) -> str:
        document = pymupdf.open(filepath)

        pages = []

        for page in document:
            pages.append(page.get_text())

        document.close()

        return "\n".join(pages).strip()