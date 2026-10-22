from datetime import datetime
from pydantic import BaseModel, ConfigDict

class Alt(BaseModel):
    category: str; confidence: float

class RecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; category: str; confidence: float; alternatives: list[Alt]; low_confidence: bool
    filename: str; model_version: str; created_at: datetime

class ClassifyOut(BaseModel):
    record: RecordOut; recommendation: dict; notice: str

class HistoryOut(BaseModel):
    items: list[RecordOut]; total: int; page: int; pages: int
