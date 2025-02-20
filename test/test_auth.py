import pytest
from fastapi import status

@pytest.mark.auth
class TestAuth:
    """Test suite for authentication-related endpoints"""

    @pytest.mark.parametrize("user_data", [
        {"username": "newuser", "password": "pass123", "is_admin": False},
        {"username": "newadmin", "password": "admin123", "is_admin": True},
    ])
    def test_register_user(self, client, user_data):
        """Test user registration"""
        response = client.post("/auth/register", json=user_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert all(key in data for key in ["message", "is_admin"])
        assert data["message"] == "User created successfully "
        assert data["is_admin"] == user_data["is_admin"]

    def test_register_duplicate_username(self, client, normal_user):
        """Test registering with an already taken username"""
        response = client.post("/auth/register", json={
            "username": normal_user.username,
            "password": "testpass123",
            "is_admin": False
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Username already exists"

    def test_login_user(self, client, normal_user):
        """Test user login with valid credentials"""
        response = client.post("/auth/login", data={
            "username": normal_user.username,
            "password": "testpass123"
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(key in data for key in ["message", "access_token", "token_type"])
        assert data["token_type"] == "bearer"
        assert data["message"] == "Logged In Successfully "

    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post("/auth/login", data={
            "username": "nonexistent",
            "password": "wrongpass"
        })
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Invalid Username Or Password"
