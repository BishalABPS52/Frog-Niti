"""
The single most important file in the project.
Every procedure in the knowledge base MUST match this schema.
Rule enforced in code: no source -> no claim.
"""
from datetime import date
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator

SourceType = Literal["official", "community_reported"]


class Source(BaseModel):
    url: str
    title: str
    last_verified: date


class Step(BaseModel):
    order: int
    action: str
    where: Optional[str] = None  # office / website
    fee: Optional[str] = None


class DocumentReq(BaseModel):
    name: str
    required: bool                      # True = required, False = optional
    reason: Optional[str] = None        # why an optional doc is useful
    source_type: SourceType = "official"


class Procedure(BaseModel):
    id: str
    title_en: str
    title_ne: Optional[str] = None
    aliases: List[str] = []             # words users might type (Nepali, English, Romanized)
    municipality: str
    office: str
    mode: Literal["online", "in_person", "both"]
    practical_tip: Optional[str] = None
    tip_source_type: SourceType = "community_reported"
    steps: List[Step]
    documents: List[DocumentReq]
    fee: Optional[str] = None
    time_needed: Optional[str] = None
    sources: List[Source] = Field(min_length=1)   # at least one source, always
    reviewed_by_human: bool = False

    @field_validator("steps")
    @classmethod
    def steps_not_empty(cls, v):
        if not v:
            raise ValueError("a procedure needs at least one step")
        return v


class AskRequest(BaseModel):
    question: str
    municipality: Optional[str] = None


class AskResponse(BaseModel):
    route: Literal["answer_from_kb", "ask_clarifying", "defer_to_office"]
    answer: str
    procedure_id: Optional[str] = None
    confidence: float = 0.0
    sources: List[Source] = []
