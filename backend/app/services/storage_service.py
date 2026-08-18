import os
import shutil
from pathlib import Path

from fastapi import UploadFile


class StorageService:

    STORAGE_DIR = Path("storage/documents")

    def __init__(self):
        self.STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    def save(self, file: UploadFile) -> str:
        filepath = self.STORAGE_DIR / file.filename

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return str(filepath)