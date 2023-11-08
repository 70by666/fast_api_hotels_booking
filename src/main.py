from fastapi import FastAPI

from src.bookings.router import router as router_bookings

app = FastAPI()

app.include_router(router_bookings)
