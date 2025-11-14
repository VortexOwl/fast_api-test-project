from pydantic import BaseModel


class IncidentSchema(BaseModel):
    description: str
    status: int
    source: str


class IncidentGetSchema(BaseModel):
    id_record: int
    description: str
    status: int
    source: str
    date_create: str


class ResponseMessage(BaseModel):
    success: bool
    message: str