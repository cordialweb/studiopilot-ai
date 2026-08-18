from pydantic import BaseModel, Field


class SceneV1(BaseModel):
    scene_number: int

    heading: str

    location: str

    time_of_day: str = ""

    page_start: int | None = None

    page_end: int | None = None

    summary: str = ""

    characters: list[str] = Field(
        default_factory=list,
        description="Characters appearing in this scene",
    )

    props: list[str] = Field(
        default_factory=list,
        description="Props appearing in this scene",
    )