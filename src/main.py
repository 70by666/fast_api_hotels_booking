from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

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

origins = [
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)
