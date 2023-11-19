import os
import shutil
from uuid import uuid4

from fastapi import UploadFile, APIRouter

from src.images.schemas import SUploadHotels
from src.images.utils import set_name

router = APIRouter(
    prefix='/images',
    tags=['Images'],
)


@router.post('/hotels', status_code=201)
async def add_hotel_image(name: int, file: UploadFile) -> SUploadHotels:
    name = set_name(name)
    with open(f'src/static/images/{name}.webp', 'wb+') as f:
        shutil.copyfileobj(file.file, f)
    # noinspection PyTypeChecker
    return {
        'status': 'success',
        'data': {
            'name': name,
        },
        'details': None,
    }
