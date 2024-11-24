from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mock_data.data import users, products, services, user_services, user_products, user_service_products
from typing import List

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

# API Endpoints
@app.get("/users", response_model=List[dict])
async def get_users():
    return users

@app.get("/products", response_model=List[dict])
async def get_products():
    return products

@app.get("/services", response_model=List[dict])
async def get_services():
    return services

@app.get("/user-services", response_model=List[dict])
async def get_user_services():
    return user_services

@app.get("/user-products", response_model=List[dict])
async def get_user_products():
    return user_products

@app.get("/user-service-products", response_model=List[dict])
async def get_user_service_products():
    return user_service_products
