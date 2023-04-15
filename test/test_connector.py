from chatgpt_connector import connector


def test_send_message():
    res = connector.send_messages([{"role": "user", "content": "test"}])
    print(res)
    assert len(res.get("choices", [])) > 0


def test_decode_response_json():
    res = connector.send_messages([{"role": "user", "content": "test"}])
    text = connector.response_to_text(res)
    assert len(text) > 0
