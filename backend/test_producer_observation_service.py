from app.adk.engine import StudioPilotEngine
from app.schemas.extraction.document import DocumentV1
from app.schemas.extraction.scene import SceneV1
from app.schemas.extraction.character import CharacterV1
from app.schemas.extraction.location import LocationV1
from app.schemas.extraction.prop import PropV1

from app.services.producer_observation_service import (
    ProducerObservationService,
)


# Build the structured screenplay information
# from the extraction we already successfully generated.

screenplay = {
    "document": {
        "title": "THE LAST LANTERN",
        "author": "Alex Morgan",
        "genre": "",
        "language": "English",
        "pages": 5,
        "summary": (
            "In the coastal town of Bellhaven, marine engineer Maya Reyes "
            "and her brother Daniel restore a failing lighthouse during a "
            "dangerous storm, uncovering hidden secrets about their missing "
            "father and his discovery of a smuggling operation."
        ),
    },

    "scenes": [
        {
            "scene_number": 5,
            "heading": "5. EXT. SEA WALL — NIGHT",
            "location": "Sea Wall",
            "time_of_day": "NIGHT",
            "page_start": 3,
            "page_end": 3,
            "summary": (
                "Lena Park tries to call Harbor Control from a fishing boat "
                "battling rough waves right as the lighthouse light abruptly "
                "goes dark."
            ),
            "characters": ["Lena Park"],
            "props": ["Handheld Radio"],
        },
        {
            "scene_number": 6,
            "heading": "6. INT. LIGHTHOUSE — LANTERN ROOM — NIGHT",
            "location": "Lighthouse — Lantern Room",
            "time_of_day": "NIGHT",
            "page_start": 3,
            "page_end": 3,
            "summary": (
                "Maya and Daniel find the lantern stopped and follow a trail "
                "of seawater to a locked maintenance hatch, which Daniel "
                "cuts open."
            ),
            "characters": ["Maya Reyes", "Daniel Reyes"],
            "props": ["Brass Lighthouse Lantern", "Pocketknife"],
        },
        {
            "scene_number": 10,
            "heading": "10. INT. LIGHTHOUSE — LANTERN ROOM — CONTINUOUS",
            "location": "Lighthouse — Lantern Room",
            "time_of_day": "CONTINUOUS",
            "page_start": 4,
            "page_end": 5,
            "summary": (
                "Maya pulls the emergency lever to restart the turning lens, "
                "beaming light to save the offshore fishing boat."
            ),
            "characters": ["Maya Reyes", "Daniel Reyes", "Lena Park"],
            "props": ["Brass Lighthouse Lantern"],
        },
    ],
}


engine = StudioPilotEngine()

service = ProducerObservationService(engine)

result = service.observe(
    screenplay_text=str(screenplay)
)

print()
print("PRODUCER OBSERVATION SERVICE SUCCESS")
print()

print(result.model_dump(mode="json"))