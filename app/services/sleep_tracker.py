# app/services/sleep_tracker.py

from datetime import datetime, timedelta

def calculate_sleep_duration(sleep_time: str, wake_time: str) -> float:
    """
    Calculate how long the user slept in hours.
    Automatically handles overnight sleep (e.g. 23:30 to 06:00).
    """
    time_format = "%H:%M"
    try:
        sleep_dt = datetime.strptime(sleep_time, time_format)
        wake_dt = datetime.strptime(wake_time, time_format)

        # Add a day if the sleep crosses midnight
        if wake_dt <= sleep_dt:
            wake_dt += timedelta(days=1)

        duration = (wake_dt - sleep_dt).total_seconds() / 3600
        return round(duration, 2)

    except Exception as e:
        raise ValueError(f"Invalid time format or logic: {e}")

def calculate_sleep_debt(actual_sleep: float, recommended_sleep: float = 8.0) -> float:
    """
    Compute sleep debt based on actual vs recommended sleep.
    Returns 0 if user met or exceeded recommended hours.
    """
    debt = recommended_sleep - actual_sleep
    return round(max(debt, 0), 2)

def generate_sleep_message(debt: float) -> str:
    """
    Generate a friendly message based on sleep debt value.
    """
    if debt == 0:
        return "🎉 Great job! You met your sleep goal."
    elif debt <= 1:
        return "🙂 Slight sleep debt. Try to rest a bit more tonight."
    else:
        return "⚠️ You're in significant sleep debt. Prioritize rest soon!"
