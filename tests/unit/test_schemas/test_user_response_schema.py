import pytest
from datetime import datetime
from app.schemas.user import UserResponse

# Test data
valid_data = {
    "id": 1,
    "email": "test@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": datetime(2023, 1, 1, 0, 0, 0),
    "updated_at": datetime(2023, 1, 1, 0, 0, 0),
}

@pytest.mark.parametrize(
    "data, should_pass",
    [
        # Valid data
        (valid_data, True),
        
        # Invalid email
        ({**valid_data, "email": "invalid-email"}, False),
        
        # Invalid first_name length
        ({**valid_data, "first_name": "A" * 51}, False),
        
        # Invalid last_name length
        ({**valid_data, "last_name": "B" * 51}, False),
        
        # Missing required fields
        ({**valid_data, "id": None}, False),
        ({**valid_data, "created_at": None}, False),
        ({**valid_data, "updated_at": None}, False),
    ],
)
def test_user_response_schema_validation(data, should_pass):
    """
    Test UserResponse schema validation.
    """
    if should_pass:
        user = UserResponse(**data)
        assert user.email == data["email"]
        assert user.first_name == data["first_name"]
        assert user.last_name == data["last_name"]
    else:
        with pytest.raises(ValueError):
            UserResponse(**data)
