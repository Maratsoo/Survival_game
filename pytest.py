import pytest
from Survivalgame import start_game, perform_action, trigger_event

# Palīgfunkcija lietotāja datiem
def create_user():
    return {
        "HP": 10,
        "еда": 0,
        "энергия": 5,
        "вода": 5,
        "предметы": [],
        "день": 1
    }

# 1. Testē /start komandu
def test_start_game():
    user_data = start_game()
    assert user_data["HP"] == 10
    assert user_data["энергия"] == 5
    assert "предметы" in user_data

# 2. Testē /hunt funkciju
def test_hunt_action():
    user = create_user()
    perform_action(user, "hunt")
    assert user["еда"] >= 1
    assert user["HP"] < 10
    assert user["энергия"] < 5

# 3. Testē nejaušo notikumu
def test_trigger_event():
    user = create_user()
    before_hp = user["HP"]
    trigger_event(user, "камень")  # vai cits atbilstošs notikums
    assert user["HP"] < before_hp

# 4. Testē priekšmetu "Telts"
def test_tent_disappears_after_lion():
    user = create_user()
    user["предметы"].append("Telts")
    trigger_event(user, "лев")
    assert "Telts" not in user["предметы"]
