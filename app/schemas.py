from typing import Annotated, Any

from pydantic import BaseModel, Field, StringConstraints


NonEmptyString = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]


class ExperimentCreate(BaseModel):
    model_name: NonEmptyString
    dataset: NonEmptyString
    parameters: dict[str, Any] = Field(default_factory=dict)
    accuracy: float = Field(ge=0.0, le=1.0)
    f1_score: float = Field(ge=0.0, le=1.0)


class ExperimentResponse(ExperimentCreate):
    id: int
    created_at: str