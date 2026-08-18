from pydantic import BaseModel, Field


class CharacterV1(BaseModel):
    name: str = Field(..., description="Character name")

    aliases: list[str] = Field(
        default_factory=list,
        description="Alternative names",
    )

    age: int | None = Field(
        default=None,
        description="Character age when explicitly stated",
    )

    occupation: str = Field(
        default="",
        description="Character occupation",
    )

    description: str = Field(
        default="",
        description="Character description",
    )

    scenes: list[int] = Field(
        default_factory=list,
        description="Scene numbers where the character appears",
    )

    first_scene: int | None = None

    last_scene: int | None = None