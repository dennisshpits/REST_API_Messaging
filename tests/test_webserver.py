import pytest
import datetime
from webserver import app, phones, messages

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clear_data():
    messages.clear()
    phones.clear()

def test_addPhone(client):
    payload = {'uni_id': '123'}
    response = client.post('/uni_id', json=payload)
    assert response.status_code == 200
    assert response.get_data(as_text=True) == 'success\n'
    assert len(phones) > 0

def test_addMessage(client):
    payload = {'uni_id': '123', 'mess': 'Hello World', 'time': datetime.datetime.utcnow().isoformat()}
    response = client.post('/sent_message', json=payload)
    assert response.status_code == 200
    assert response.get_data(as_text=True) == 'success\n'
    assert len(messages) > 0

