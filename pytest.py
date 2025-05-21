import pytest
from game import start_game, perform_action, trigger_event  # Импортируй свои функции

def user():
    return {
        "HP": 10,
        "еда": 0,
        "энергия": 5,
        "вода": 5,
        "предметы": [],
        "день": 1
    }

# 1. Тест /start
def test_start_game():
    user_data = start_game()
    assert user_data["HP"] == 10
    assert user_data["энергия"] == 5
    assert "предметы" in user_data

# 2. Тест /hunt
def test_hunt_action(user):
    result = perform_action(user, "hunt")
    assert user["еда"] >= 1
    assert user["HP"] < 10
    assert user["энергия"] < 5

# 3. Тест случайного события
def test_trigger_event(user):
    user["предметы"] = []
    before_hp = user["HP"]
    trigger_event(user, "dropped rock")  # Например, событие «камень»
    assert user["HP"] < before_hp

# 4. Тест палатки (Telts)
def test_tent_disappears_after_lion(user):
    user["предметы"] = ["Telts"]
    trigger_event(user, "лев")
    assert "Telts" not in user["предметы"]
