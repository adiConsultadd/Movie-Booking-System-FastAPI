import pytest
from fastapi import status


@pytest.mark.user
class TestUser:
    """Test suite for user-related endpoints"""

    def test_view_all_movies(self, client, normal_user_token):
        """Test viewing available movies as a normal user"""
        response = client.get(
            "/movies", headers={"Authorization": f"Bearer {normal_user_token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        movies = response.json()
        assert isinstance(movies, list)
        if movies:
            assert all(key in movies[0] for key in ["title", "showtime"])

    @pytest.mark.parametrize("movie_id", [-1, 9999, 0])
    def test_book_movie_invalid_id(self, client, normal_user_token, movie_id):
        """Test booking movies with invalid movie IDs"""
        response = client.post(
            f"/movies/{movie_id}/book",
            headers={"Authorization": f"Bearer {normal_user_token}"},
            json={"movie_id": movie_id},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_book_movie_success(self, client, normal_user_token, test_movie):
        """Test successful movie booking"""
        movie_id = test_movie.id
        response = client.post(
            f"/movies/{movie_id}/book",
            headers={"Authorization": f"Bearer {normal_user_token}"},
            json={"movie_id": movie_id},
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        print(data)
        assert all(key in data for key in ["message", "booking"])
        assert data["message"] == "Ticket booked successfully"
        assert data.get("booking").get("movie_id") == movie_id

    def test_book_movie_duplicate(self, client, normal_user_token, mock_booking):
        """Test booking same movie twice"""
        movie_id = mock_booking.id
        response = client.post(
            f"/movies/{movie_id}/book",
            headers={"Authorization": f"Bearer {normal_user_token}"},
            json={"movie_id": movie_id},
        )
        data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert data.get("detail") == "You have already booked this movie"

    def test_cancel_booking_success(self, client, normal_user_token, mock_booking):
        """Test successful booking cancellation"""
        movie_id = mock_booking.movie_id
        response = client.delete(
            f"/movies/{movie_id}/cancel",
            headers={"Authorization": f"Bearer {normal_user_token}"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.parametrize("movie_id", [-1, 9999, 0])
    def test_cancel_nonexistent_booking(self, client, movie_id, normal_user_token):
        """Test canceling a booking that doesn't exist"""
        response = client.delete(
            f"/movies/{movie_id}/cancel",
            headers={"Authorization": f"Bearer {normal_user_token}"},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_view_booking_history(self, client, normal_user_token):
        """Test viewing user's booking history"""
        response = client.get(
            "/movies/history", headers={"Authorization": f"Bearer {normal_user_token}"}
        )
        assert response.status_code == status.HTTP_200_OK
        bookings = response.json()
        assert isinstance(bookings, list)
        if bookings:
            assert all(key in bookings[0] for key in ["user_id", "movie_id"])
