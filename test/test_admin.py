import pytest
from fastapi import status

@pytest.mark.admin
class TestAdminRoutes:
    """Test suite for admin-related endpoints"""

    def test_create_new_movie(self, client, admin_token, test_movie_data):
        """Test adding a new movie to the database"""
        response = client.post(
            "/admin/movies",
            headers={"Authorization": f"Bearer {admin_token}"},
            json=test_movie_data
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert all(key in data for key in ["message", "movie"])
        assert all(key in data["movie"] for key in ["title", "description", "showtime"])

    def test_view_all_movies(self, client, admin_token):
        """Test viewing all movies present in the database"""
        response = client.get(
            "/admin/movies",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        movies = response.json()
        assert isinstance(movies, list)
        if movies:
            assert all(key in movies[0] for key in ["title", "description", "showtime"])

    @pytest.mark.parametrize("invalid_data", [
        {"title": None, "description": "Test", "showtime": "2024-02-21 10:00:00"},
        {"title": "Test", "description": None, "showtime": "2024-02-21 10:00:00"},
        {"title": "Test", "description": "Test", "showtime": None}
    ])
    def test_create_new_movie_validation(self, client, admin_token, invalid_data):
        """Test creating a movie with invalid data"""
        response = client.post(
            "/admin/movies",
            headers={"Authorization": f"Bearer {admin_token}"},
            json=invalid_data
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
