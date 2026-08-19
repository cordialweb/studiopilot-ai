import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


class StorageService:

    STORAGE_DIR = Path("storage/documents")

    def __init__(self):
        self.STORAGE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(self, file: UploadFile) -> str:
        original_name = Path(
            file.filename or "document.pdf"
        ).name

        unique_name = (
            f"{uuid4().hex}_{original_name}"
        )

        filepath = self.STORAGE_DIR / unique_name

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        return str(filepath)