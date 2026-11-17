import pytest
from app.core.cache import STUDENT_CACHE
from app.core.state_machine import process_ussd_session

@pytest.fixture(autouse=True)
def setup_test_cache():
    # Seed known test student
    STUDENT_CACHE["+254712345678"] = {
        "student_id": "STU001",
        "name": "Jane Doe",
        "fees_due": "KES 15,000",
        "attendance": "95% (Present 38/40 days)",
        "latest_grade": "Mathematics: A, English: B+, Science: A-"
    }
    yield
    # Cleanup
    STUDENT_CACHE.pop("+254712345678", None)


def test_ussd_initial_dial_shows_main_menu():
    response = process_ussd_session(phone_number="+254712345678", text="")
    assert response.startswith("CON")
    assert "Jane Doe" in response
    assert "1. Check Fee Balance" in response
    assert "2. View Attendance" in response
    assert "3. View Recent Grades" in response


def test_ussd_select_fee_balance():
    response = process_ussd_session(phone_number="+254712345678", text="1")
    assert response.startswith("END")
    assert "Fee Balance for Jane Doe" in response
    assert "KES 15,000" in response


def test_ussd_select_attendance():
    response = process_ussd_session(phone_number="+254712345678", text="2")
    assert response.startswith("END")
    assert "Attendance Record for Jane Doe" in response
    assert "95%" in response


def test_ussd_select_recent_grades():
    response = process_ussd_session(phone_number="+254712345678", text="3")
    assert response.startswith("END")
    assert "Recent Grades for Jane Doe" in response
    assert "Mathematics: A" in response


def test_ussd_invalid_option():
    response = process_ussd_session(phone_number="+254712345678", text="99")
    assert response.startswith("END")
    assert "Invalid choice" in response


def test_ussd_unregistered_phone_number():
    response = process_ussd_session(phone_number="+254799999999", text="")
    assert response.startswith("END")
    assert "not registered" in response
