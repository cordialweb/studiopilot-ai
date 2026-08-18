from pydantic import BaseModel, Field


class LocationV1(BaseModel):
    name: str

    type: str = ""

    interior_exterior: str = ""

    description: str = ""

    scenes: list[int] = Field(
        default_factory=list,
        description="Scene numbers where the location appears",
    )

    scene_count: int = 0