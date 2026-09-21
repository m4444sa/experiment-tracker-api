
# describing the shape of the data to fastAPI
from typing import Annotated, Any

from pydantic import BaseModel, Field, StringConstraints


NonEmptyString = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
] #reusable string type


class ExperimentCreate(BaseModel): #pydantic data model
    model_name: NonEmptyString
    dataset: NonEmptyString
    parameters: dict[str, Any] = Field(default_factory=dict)
    accuracy: float = Field(ge=0.0, le=1.0)
    f1_score: float = Field(ge=0.0, le=1.0) #upper and lower bounds 


class ExperimentResponse(ExperimentCreate):
    id: int
    created_at: str