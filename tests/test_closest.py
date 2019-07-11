from apistar import TestClient

from app import app


def test_reverse():
    client = TestClient(app)
    response = client.get('http://localhost/v1/reverse/48.810273:5.108632')

    assert response.status_code == 200
    assert response.json()['id'] == 'addr:5.108632;48.810273'
    assert response.json()['name'] == '4 Rue du Moulin'


def test_place_latlon():
    client = TestClient(app)
    response = client.get('http://localhost/v1/places/latlon:48.810105:5.108788')

    assert response.status_code == 200
    response_data = response.json()
    assert response_data['id'] == 'latlon:48.81011:5.10879'
    assert response_data['name'] == '48.81011 : 5.10879'
    assert response_data['geometry']['center'] == [5.10879, 48.81011]
    assert response_data['address']['label'] == "4 Rue du Moulin (Val-d'Ornain)"


def test_place_latlon_no_address():
    client = TestClient(app)
    response = client.get('http://localhost/v1/places/latlon:-48.810273:35.108632')

    assert response.status_code == 200
    response_data = response.json()
    assert response_data['id'] == 'latlon:-48.81027:35.10863'
    assert response_data['name'] == '-48.81027 : 35.10863'
    assert response_data['geometry']['center'] == [35.10863, -48.81027]
    assert response_data['address'] is None