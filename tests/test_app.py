from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_home_page():

    response = client.get("/")

    assert response.status_code == 200

    assert "EduGenie" in response.text


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

    assert data["service"] == "EduGenie"


def test_quiz_clean_json_block():

    from quiz_module import clean_json_block

    raw = """
    ```json
    [
        {
            "question": "2+2?",
            "options": [
                "1",
                "2",
                "3",
                "4"
            ],
            "correct_answer": "4",
            "explanation": "2 + 2 = 4."
        }
    ]
    ```
    """

    cleaned = clean_json_block(raw)

    assert cleaned.startswith("[")

    assert cleaned.endswith("]")


def test_quiz_clean_plain_json():

    from quiz_module import clean_json_block

    raw = """
    [
        {
            "question": "What is Python?",
            "options": [
                "Language",
                "Car",
                "Food",
                "Country"
            ],
            "correct_answer": "Language",
            "explanation": "Python is a programming language."
        }
    ]
    """

    cleaned = clean_json_block(raw)

    assert cleaned.startswith("[")

    assert cleaned.endswith("]")