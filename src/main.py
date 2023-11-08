from fastapi import FastAPI

from src.bookings.router import router as router_bookings
from src.auth.router import router as router_auth

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_bookings)
