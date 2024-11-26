from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import routers  # Import the routers list from the endpoints module

app = FastAPI()

# Add CORS Middleware
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers from the endpoints
for route in routers:
    app.include_router(route["router"], prefix=route["prefix"], tags=route["tags"])

