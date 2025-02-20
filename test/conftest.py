import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta

from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.models.movie import Movie
from app.utils.security import create_hash, create_access_token
from app.models.booking import Booking

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Creates and cleans up a fresh test database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Provides a test client with a fresh database session"""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

# Mock data fixtures
@pytest.fixture
def test_movie_data():
    """Provides sample movie data for tests"""
    return {
        "title": "Test Movie",
        "description": "Test Description",
        "showtime": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    }

@pytest.fixture
def normal_user(db_session):
    """Creates a normal user for testing"""
    user = User(username="testuser", hashed_password=create_hash("testpass123"), is_admin=False)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def admin_user(db_session):
    """Creates an admin user for testing"""
    admin = User(username="adminuser", hashed_password=create_hash("adminpass123"), is_admin=True)
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin

@pytest.fixture
def test_movie(db_session, test_movie_data):
    """Creates a test movie entry that can be reused"""
    movie = Movie(**test_movie_data)
    db_session.add(movie)
    db_session.commit()
    db_session.refresh(movie)
    return movie

@pytest.fixture
def mock_booking(db_session, normal_user, test_movie):
    """Creates a mock booking for testing"""
    booking = Booking(user_id=normal_user.id, movie_id=test_movie.id)
    db_session.add(booking)
    db_session.commit()
    db_session.refresh(booking)
    return booking

@pytest.fixture
def normal_user_token(normal_user):
    """Generates an access token for a normal user"""
    return create_access_token(
        str(normal_user.username), normal_user.id, normal_user.is_admin, timedelta(minutes=20)
    )

@pytest.fixture
def admin_token(admin_user):
    """Generates an access token for an admin user"""
    return create_access_token(
        str(admin_user.username), admin_user.id, admin_user.is_admin, timedelta(minutes=20)
    )
