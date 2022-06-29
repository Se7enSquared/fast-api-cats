from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

yoda = {
    "name": "Yoda",
    "age": 4,
    "color": "black",
    "temperament": "shy",
    "weight_in_lbs": 6.2,
    "description": "Yoda is a shy but sweet black Manx with long-hair and a "
    "natural half-tail",
    "image": "/static/img/yoda.jpg"
}

new_cat = {
    "name": "Tiger",
    "age": 7,
    "color": "orange",
    "temperament": "picky",
    "weight_in_lbs": 5.2,
    "description": "Tiger only likes salmon flavored foods",
    "image": None
}

cats = {
    "1": {
        "name": "Yoda",
        "age": 4,
        "color": "black",
        "temperament": "shy",
        "weight_in_lbs": 6.2,
        "description": "Yoda is a shy but sweet black Manx with long-hair and a natural half-tail",
        "image": "/static/img/yoda.jpg"
    },
    "2": {
        "name": "Pebbles",
        "age": 4,
        "color": "tabby",
        "temperament": "active",
        "weight_in_lbs": 9.4,
        "description": "Pebbles is a fast, active bobtail kitty with a strong hunting drive",
        "image": "/static/img/pebbles.jpg"
    },
    "3": {
        "name": "Coral",
        "age": 2,
        "color": "Grey stripe",
        "temperament": "hyper",
        "weight_in_lbs": 9.4,
        "description": "Coral is part bengal and loves to jump for her toys",
        "image": "/static/img/coral.jpg"
    }
}


def test_get_cats():
    response = client.get('/get-cats/')
    assert response.status_code == 200
    assert response.json() == cats


def test_get_cat():
    response = client.get('/get-cat/1')
    assert response.status_code == 200


def test_get_wrong_cat():
    response = client.get('/get-cat/100')
    assert response.status_code == 404


def test_get_cat_by_name():
    response = client.get('/get-by-name/?name=yoda')
    assert response.status_code == 200
    assert response.json() == yoda


def test_get_cat_by_wrong_name():
    response = client.get('/get-by-name/?name=jingles')
    assert response.status_code == 200
    assert response.json() == {}


def test_add_cat():
    response = client.post('/add-cat/', json=new_cat)
    assert response.status_code == 200
    assert response.json() == new_cat
