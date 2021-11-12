import json

def test_get_messages(client):
    data = {
        "message": "message v1"
    }
    response = client.simulate_get("/v1/message")
    assert json.loads(response.content) == data


def test_get_message_by_id(client):
    message_id = 1
    data = {
        "message": f"message v2 for {message_id}"
    }
    response = client.simulate_get(f"/v2/message/{message_id}")
    assert json.loads(response.content) == data

