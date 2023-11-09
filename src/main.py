from fastapi import FastAPI

from src.bookings.router import router as router_bookings
from src.auth.router import router as router_auth
from src.hotels.router import router as router_hotels
from src.hotels.rooms.router import router as router_rooms

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
