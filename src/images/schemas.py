from typing import Optional

from pydantic import BaseModel


class SUploadHotels(BaseModel):
    status: str
    data: Optional[str]
    details: Optional[str]
