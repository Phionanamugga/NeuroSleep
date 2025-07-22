from datetime import datetime, timedelta
from app.services.recommender import SleepRecommender
from app.db.models import SleepLog

class DummyDBSession:
    def query(self, model):
        class Query:
            def filter(self, *args, **kwargs):
                return self

            def all(self):
                return [
                    SleepLog(date=datetime.today().date() - timedelta(days=i), sleep_duration=6.0)
                    for i in range(7)
                ]
        return Query()

def test_get_recommendation():
    recommender = SleepRecommender(DummyDBSession())
    result = recommender.get_recommendation("07:00")
    assert "sleep_debt_hours" in result
    assert "recommended_bedtime" in result
    assert isinstance(result["sleep_debt_hours"], float)
