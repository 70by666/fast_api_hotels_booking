import os
import shutil
from uuid import uuid4

from fastapi import UploadFile, APIRouter

from src.images.schemas import SUploadHotels
from src.images.utils import set_name
from src.tasks.tasks import process_pic

router = APIRouter(
    prefix='/images',
    tags=['Images'],
)


@router.post('/hotels', status_code=201)
async def add_hotel_image(name: int, file: UploadFile) -> SUploadHotels:
    name = set_name(name)
    path = f'src/static/images/{name}.webp'
    with open(path, 'wb+') as f:
        shutil.copyfileobj(file.file, f)
    process_pic.delay(path)
    # noinspection PyTypeChecker
    return {
        'status': 'success',
        'data': {
            'name': name,
        },
        'details': None,
    }
