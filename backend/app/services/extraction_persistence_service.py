from sqlalchemy.orm import Session

from app.models.character import Character
from app.models.location import Location
from app.models.prop import Prop
from app.models.scene import Scene
from app.schemas.extraction.result import ExtractionResultV1


class ExtractionPersistenceService:

    def __init__(self, db: Session):
        self.db = db

    def save(
        self,
        document_id: int,
        result: ExtractionResultV1,
    ):
        # Characters
        for character in result.characters:
            db_character = Character(
                document_id=document_id,
                name=character.name,
                aliases=character.aliases,
                age=character.age,
                occupation=character.occupation,
                description=character.description,
                scenes=character.scenes,
                first_scene=character.first_scene,
                last_scene=character.last_scene,
            )

            self.db.add(db_character)

        # Locations
        for location in result.locations:
            db_location = Location(
                document_id=document_id,
                name=location.name,
                type=location.type,
                interior_exterior=location.interior_exterior,
                description=location.description,
                scenes=location.scenes,
                scene_count=location.scene_count,
            )

            self.db.add(db_location)

        # Props
        for prop in result.props:
            db_prop = Prop(
                document_id=document_id,
                name=prop.name,
                category=prop.category,
                description=prop.description,
                scenes=prop.scenes,
                scene_count=prop.scene_count,
            )

            self.db.add(db_prop)

        # Scenes
        for scene in result.scenes:
            db_scene = Scene(
                document_id=document_id,
                scene_number=scene.scene_number,
                heading=scene.heading,
                location=scene.location,
                time_of_day=scene.time_of_day,
                page_start=scene.page_start,
                page_end=scene.page_end,
                summary=scene.summary,
                characters=scene.characters,
                props=scene.props,
            )

            self.db.add(db_scene)

        self.db.commit()

        return result