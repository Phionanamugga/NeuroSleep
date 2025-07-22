# test_db.py

'''from app.db.database import SessionLocal
from app.db.models import SleepLog
from datetime import date

def test_db():
    db = SessionLocal()
    try:
        # Insert
        sleep_log = SleepLog(
            date=date.today(),
            sleep_time="22:30",
            wake_time="06:30",
            sleep_duration=8.0
        )
        db.add(sleep_log)
        db.commit()

        # Query
        result = db.query(SleepLog).filter(SleepLog.date == date.today()).first()
        print(f"Queried Sleep Log: {result.date}, Duration: {result.sleep_duration} hours")

    finally:
        db.close()

if __name__ == "__main__":
    test_db()'''
# This script tests basic database operations: inserting and querying a sleep log.
# It uses the SQLAlchemy ORM to interact with the database.
# Make sure your database is set up and the models are created before running this test.

from app.db.database import SessionLocal, engine, Base
from app.db.models import SleepLog
from datetime import date

def test_db():
    # Ensure tables are created
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Insert a sleep log
        sleep_log = SleepLog(
            date=date.today(),
            sleep_time="22:30",
            wake_time="06:30",
            sleep_duration=8.0
        )
        db.add(sleep_log)
        db.commit()

        # Fetch and verify the log
        result = db.query(SleepLog).filter_by(date=date.today()).first()
        assert result is not None
        assert result.sleep_duration == 8.0

    finally:
        db.close()
