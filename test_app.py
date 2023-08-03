import pytest
from backend import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_initial_state(client):
    response = client.get('/')
    data = response.get_json()
    assert response.status_code == 200
    assert data['state'] == 'locked'
    assert data['message'] == 'Дверь закрыта. Введите пароль'

def test_unlock_incorrect_password(client):
    response = client.post('/unlock', json={'password': {'password': 'wrong'}})
    data = response.get_json()
    assert response.status_code == 200
    assert data['state'] == 'locked'
    assert data['message'] == 'Пароль неверный'
    
def test_unlock_correct_password(client):
    response = client.post('/unlock', json={'password': {'password': '1234'}})
    data = response.get_json()
    assert response.status_code == 200
    assert data['state'] == 'unlocked'
    assert data['message'] == 'Дверь открыта'

def test_lock_door(client):
    response = client.post('/lock')
    data = response.get_json()
    assert response.status_code == 200
    assert data['state'] == 'locked'
    assert data['message'] == 'Дверь закрыта. Введите пароль'
