from pydantic import BaseModel

from app.schemas.extraction.document import DocumentV1
from app.schemas.extraction.scene import SceneV1
from app.schemas.extraction.character import CharacterV1
from app.schemas.extraction.location import LocationV1
from app.schemas.extraction.prop import PropV1


class ExtractionResultV1(BaseModel):
    document: DocumentV1
    scenes: list[SceneV1] = []
    characters: list[CharacterV1] = []
    locations: list[LocationV1] = []
    props: list[PropV1] = []