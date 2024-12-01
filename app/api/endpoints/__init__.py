from app.api.endpoints.users import router as users_router
from app.api.endpoints.products import router as products_router
from app.api.endpoints.services import router as services_router
from app.api.endpoints.auth import router as auth_router
# Combine all routers in a list for easier imports
routers = [
    {"router": users_router, "prefix": "/api/v1", "tags": ["users"]},
    {"router": products_router, "prefix": "/api/v1", "tags": ["products"]},
    {"router": services_router, "prefix": "/api/v1", "tags": ["services"]},
    {"router": auth_router, "prefix": "/api/v1", "tags": ["auth"]},
]
