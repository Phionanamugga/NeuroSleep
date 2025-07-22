import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.models.user import User
from app.models.user_data import UserData

# Create an in-memory SQLite DB for tests
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_create_user_and_userdata(db_session):
    # Create a user
    user = User(username="testuser", email="test@example.com", hashed_password="fakehashed")
    db_session.add(user)
    db_session.commit()

    # Create user data linked to user
    userdata = UserData(user_id=user.id, sleep_goal=7.5, preferred_wake_time="06:30")
    db_session.add(userdata)
    db_session.commit()

    # Check relationship
    assert userdata.user == user
    assert user.user_data == userdata
    assert userdata.sleep_goal == 7.5
    assert userdata.preferred_wake_time == "06:30"
