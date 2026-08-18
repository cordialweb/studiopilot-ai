from pydantic import BaseModel, Field


class PropV1(BaseModel):
    name: str

    category: str = ""

    description: str = ""

    scenes: list[int] = Field(
        default_factory=list,
        description="Scene numbers where the prop appears",
    )

    scene_count: int = 0