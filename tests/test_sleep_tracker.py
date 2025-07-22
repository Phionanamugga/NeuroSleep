# tests/test_sleep_tracker.py

import pytest
from app.services.sleep_tracker import (
    calculate_sleep_duration,
    calculate_sleep_debt,
    generate_sleep_message
)

def test_calculate_sleep_duration_normal():
    assert calculate_sleep_duration("22:00", "06:00") == 8.0

def test_calculate_sleep_duration_overnight():
    assert calculate_sleep_duration("23:30", "07:15") == 7.75

def test_calculate_sleep_duration_invalid():
    with pytest.raises(ValueError):
        calculate_sleep_duration("invalid", "07:00")

def test_calculate_sleep_debt_zero_debt():
    assert calculate_sleep_debt(8.0, 8.0) == 0

def test_calculate_sleep_debt_some_debt():
    assert calculate_sleep_debt(6.5, 8.0) == 1.5

def test_generate_sleep_message_good():
    assert generate_sleep_message(0) == "🎉 Great job! You met your sleep goal."

def test_generate_sleep_message_light_debt():
    assert generate_sleep_message(0.8) == "🙂 Slight sleep debt. Try to rest a bit more tonight."

def test_generate_sleep_message_high_debt():
    assert generate_sleep_message(3.0) == "⚠️ You're in significant sleep debt. Prioritize rest soon!"

