users = [
    {"id": 1, "email": "john.doe@example.com", "first_name": "John", "last_name": "Doe", "created_at": "2024-01-01T10:00:00Z", "updated_at": "2024-01-01T10:00:00Z"},
    {"id": 2, "email": "jane.smith@example.com", "first_name": "Jane", "last_name": "Smith", "created_at": "2024-01-02T12:00:00Z", "updated_at": "2024-01-02T12:00:00Z"},
    {"id": 3, "email": "alice.jones@example.com", "first_name": "Alice", "last_name": "Jones", "created_at": "2024-01-03T15:00:00Z", "updated_at": "2024-01-03T15:00:00Z"}
]

products = [
    {"id": 1, "title": "Shampoo", "description": "Gentle cleansing shampoo for all hair types.", "amount": 15.99},
    {"id": 2, "title": "Conditioner", "description": "Moisturizing conditioner for dry hair.", "amount": 18.99},
    {"id": 3, "title": "Hair Serum", "description": "Nourishing serum for frizz control and shine.", "amount": 25.99}
]

services = [
    {"id": 1, "title": "Haircut", "description": "Professional haircut tailored to your style.", "amount": 30.00},
    {"id": 2, "title": "Hair Coloring", "description": "Custom hair coloring and highlights.", "amount": 70.00},
    {"id": 3, "title": "Scalp Treatment", "description": "Revitalizing scalp treatment for healthy hair.", "amount": 40.00}
]

user_services = [
    {"user_id": 1, "service_id": 1},
    {"user_id": 1, "service_id": 2},
    {"user_id": 2, "service_id": 3},
    {"user_id": 3, "service_id": 1},
    {"user_id": 3, "service_id": 3}
]

user_products = [
    {"user_id": 1, "product_id": 2},
    {"user_id": 1, "product_id": 3},
    {"user_id": 2, "product_id": 1},
    {"user_id": 3, "product_id": 1},
    {"user_id": 3, "product_id": 2}
]

user_service_products = [
    {"user_id": 1, "service_id": 1, "product_id": 2},
    {"user_id": 1, "service_id": 2, "product_id": 3},
    {"user_id": 2, "service_id": 3, "product_id": 1},
    {"user_id": 3, "service_id": 1, "product_id": 2},
    {"user_id": 3, "service_id": 3, "product_id": 3}
]