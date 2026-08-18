from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.scene import Scene
from app.models.character import Character
from app.models.location import Location
from app.models.prop import Prop


router = APIRouter(
    prefix="/documents",
    tags=["Document Extraction"],
)


@router.get("/{document_id}/scenes")
def get_document_scenes(
    document_id: int,
    db: Session = Depends(get_db),
):
    scenes = (
        db.query(Scene)
        .filter(Scene.document_id == document_id)
        .order_by(Scene.scene_number)
        .all()
    )

    return {
        "document_id": document_id,
        "count": len(scenes),
        "scenes": [
            {
                "id": scene.id,
                "scene_number": scene.scene_number,
                "heading": scene.heading,
                "location": scene.location,
                "time_of_day": scene.time_of_day,
                "page_start": scene.page_start,
                "page_end": scene.page_end,
                "summary": scene.summary,
                "characters": scene.characters,
                "props": scene.props,
            }
            for scene in scenes
        ],
    }


@router.get("/{document_id}/characters")
def get_document_characters(
    document_id: int,
    db: Session = Depends(get_db),
):
    characters = (
        db.query(Character)
        .filter(Character.document_id == document_id)
        .order_by(Character.first_scene)
        .all()
    )

    return {
        "document_id": document_id,
        "count": len(characters),
        "characters": [
            {
                "id": character.id,
                "name": character.name,
                "aliases": character.aliases,
                "age": character.age,
                "occupation": character.occupation,
                "description": character.description,
                "scenes": character.scenes,
                "first_scene": character.first_scene,
                "last_scene": character.last_scene,
            }
            for character in characters
        ],
    }


@router.get("/{document_id}/locations")
def get_document_locations(
    document_id: int,
    db: Session = Depends(get_db),
):
    locations = (
        db.query(Location)
        .filter(Location.document_id == document_id)
        .order_by(Location.name)
        .all()
    )

    return {
        "document_id": document_id,
        "count": len(locations),
        "locations": [
            {
                "id": location.id,
                "name": location.name,
                "type": location.type,
                "interior_exterior": location.interior_exterior,
                "description": location.description,
                "scenes": location.scenes,
                "scene_count": location.scene_count,
            }
            for location in locations
        ],
    }


@router.get("/{document_id}/props")
def get_document_props(
    document_id: int,
    db: Session = Depends(get_db),
):
    props = (
        db.query(Prop)
        .filter(Prop.document_id == document_id)
        .order_by(Prop.name)
        .all()
    )

    return {
        "document_id": document_id,
        "count": len(props),
        "props": [
            {
                "id": prop.id,
                "name": prop.name,
                "category": prop.category,
                "description": prop.description,
                "scenes": prop.scenes,
                "scene_count": prop.scene_count,
            }
            for prop in props
        ],
    }