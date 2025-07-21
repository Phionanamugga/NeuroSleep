from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.models import SleepLog

class SleepRecommender:
    def __init__(self, db: Session):
        self.db = db

    def calculate_sleep_debt(self, ideal_duration: float = 8.0) -> float:
        """Calculate accumulated sleep debt over the past 7 days."""
        today = datetime.today().date()
        week_ago = today - timedelta(days=7)

        logs = (
            self.db.query(SleepLog)
            .filter(SleepLog.date >= week_ago)
            .all()
        )

        actual_total = sum(log.sleep_duration for log in logs)
        ideal_total = ideal_duration * 7

        debt = ideal_total - actual_total
        return round(debt, 2)

    def recommend_bedtime(self, wake_time: str, sleep_debt: float) -> str:
        """
        Suggest an ideal bedtime to reduce sleep debt.
        Wake time format: "HH:MM"
        """
        wake_dt = datetime.strptime(wake_time, "%H:%M")
        recommended_sleep = 8.0 + min(sleep_debt, 2.0)  # up to 2h recovery

        bedtime_dt = wake_dt - timedelta(hours=recommended_sleep)
        return bedtime_dt.strftime("%H:%M")

    def get_recommendation(self, wake_time: str = "07:00") -> dict:
        debt = self.calculate_sleep_debt()
        recommended_bedtime = self.recommend_bedtime(wake_time, debt)
        return {
            "sleep_debt_hours": debt,
            "recommended_bedtime": recommended_bedtime,
            "message": (
                "You're sleep-deprived. Aim to sleep earlier!" if debt > 0 else
                "You're on track. Maintain your routine!"
            )
        }
