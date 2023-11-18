import shutil

from fastapi import UploadFile, APIRouter

from src.images.schemas import SUploadHotels

router = APIRouter(
    prefix='/images',
    tags=['Images'],
)


@router.post('/hotels')
async def add_hotel_image(name: int, file: UploadFile) -> SUploadHotels:
    with open(f'src/static/images/{name}.webp', 'wb+') as f:
        shutil.copyfileobj(file.file, f)
    # noinspection PyTypeChecker
    return {
        'status': 'success',
        'data': None,
        'details': None,
    }
