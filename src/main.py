from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.bookings.router import router as router_bookings
from src.auth.router import router as router_auth
from src.hotels.router import router as router_hotels
from src.hotels.rooms.router import router as router_rooms
from src.pages.router import router as router_pages
from src.images.router import router as router_images

app = FastAPI()

app.mount('/static', StaticFiles(directory='src/static'), 'static')

app.include_router(router_auth)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_images)
