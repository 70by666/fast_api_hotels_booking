from typing import Optional

from pydantic import BaseModel


class SUploadHotelsData(BaseModel):
    name: str


class SUploadHotels(BaseModel):
    status: str
    data: SUploadHotelsData
    details: Optional[str]
