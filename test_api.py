import pytest
from flask import json
from api import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_empty(client):
    rv = client.get('/')
    assert b"GoodReads API home page" in rv.data


def test_get_book(client):
    res = client.get('/book?id=2767052')
    assert res.status_code == 200
    expected = 'The Hunger Games'
    res_data = json.loads(res.get_data(as_text=True))[0]['title']
    assert expected == res_data

    res1 = client.get('/book?id=hahahaha')
    assert res1.status_code == 404

    res2 = client.get('/book?xx')
    assert res2.status_code == 400


def test_get_author(client):
    res = client.get('/author?id=1077326')
    assert res.status_code == 200
    res_data = json.loads(res.get_data(as_text=True))[0]['name']
    expected = 'J.K. Rowling'
    assert expected == res_data

    res1 = client.get('/author?id=hahahaha')
    assert res1.status_code == 404

    res2 = client.get('/author?xx')
    assert res2.status_code == 400


def test_search_query(client):
    res1 = client.get('/search?q=books.rating_count:>15000AND<20000')
    expected = 13
    res1_data = json.loads(res1.get_data())
    assert expected == len(res1_data)

    res2 = client.get('/search?q=books.rating_count:NOT<4000000')
    expected = 4
    res2_data = json.loads(res2.get_data())
    assert expected == len(res2_data)

    res3 = client.get('/search?q=books.book_id:"41865"')
    assert res3.status_code == 200
    expected = 'Twilight'
    res3_data = json.loads(res3.get_data())[0]['title']
    assert expected == res3_data


def test_put_book(client):
    res1 = client.put('/book?id=3', data=json.dumps({"ISBN": "0590353403"}),
                      content_type='application/json')
    assert res1.status_code == 200
    res1_data = json.loads(res1.get_data())[0]
    assert "Harry Potter and the Sorcerer's Stone" == res1_data['title']
    assert '0590353403' == res1_data['ISBN']


def test_put_author(client):
    res1 = client.put('/author?id=1265', data=json.dumps({"review_count": "183820"}),
                      content_type='application/json')
    assert res1.status_code == 200
    res1_data = json.loads(res1.get_data())[0]
    assert 'Jane Austen' == res1_data['name']
    assert '183820' == res1_data['review_count']

    res2 = client.get('/author?id=yayayaya')
    assert res2.status_code == 404


def test_post_book(client):
    to_insert = {
        "book_url":
            "https://www.goodreads.com/book/show/4214.Life_of_Pi",
        "title": "Life of Pi", "book_id": "4214", "ISBN": "9780770430078",
        "author_url": "https://www.goodreads.com/author/show/811.Yann_Martel",
        "author": "Yann Martel", "rating": 3.92,
        "rating_count": 1382964, "review_count": 47781,
        "image_url":
            "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1320562005l/4214.jpg",
        "similar_books": ["https://www.goodreads.com/book/show/77203.The_Kite_Runner"]
    }

    res = client.post('/book', data=json.dumps([to_insert]),
                      content_type='application/json')
    assert res.status_code == 201
    get_res = client.get('/book?id=4214')
    assert get_res.status_code == 200


def test_post_books(client):
    to_insert = [
        {"book_url": "https://www.goodreads.com/book/show/1420.Hamlet",
         "title": "Hamlet", "book_id": "1420", "rating_count": 10000
         }, {
            "book_url":
                "https://www.goodreads.com/book/show/1381.The_Odyssey",
            "title": "The Odyssey", "book_id": "1381", "rating_count": 10000
        }
    ]

    res1 = client.post('/books', data=json.dumps(to_insert),
                       content_type='application/json')
    assert res1.status_code == 201
    get_res1 = client.get('/book?id=1420')
    assert get_res1.status_code == 200
    get_res2 = client.get('/book?id=1381')
    assert get_res2.status_code == 200

    res2 = client.post('/books', data=json.dumps([{"text": "not valid"}]),
                       content_type='application/json')
    assert res2.status_code == 400


def test_post_author(client):
    to_insert = {
        "name": "Homer",
        "author_url": "https://www.goodreads.com/author/show/903.Homer",
        "author_id": "903", "rating": 3.78, "rating_count": 888200,
        "review_count": 12891
    }
    res = client.post('/author', data=json.dumps([to_insert]),
                      content_type='application/json')
    assert res.status_code == 201
    get_res = client.get('/author?id=903')
    assert get_res.status_code == 200


def test_post_authors(client):
    to_insert = [
        {"name": "Homer",
         "author_url": "https://www.goodreads.com/author/show/903.Homer",
         "author_id": "903", "rating_count": 10000
         }, {
            "name": "Robert Fagles",
            "author_url": "https://www.goodreads.com/author/show/1005.Robert_Fagles",
            "author_id": "1005", "rating_count": 10000
        }
    ]
    res1 = client.post('/authors', data=json.dumps(to_insert),
                       content_type='application/json')
    assert res1.status_code == 201
    get_res1 = client.get('/author?id=903')
    assert get_res1.status_code == 200

    res2 = client.post('/authors', data=json.dumps([{"text": "not valid"}]),
                       content_type='application/json')
    assert res2.status_code == 400


def test_scrape_book(client):
    res = client.post('/scrape/book?id=52578297')
    assert res.status_code == 200
    get_res = client.get('/book?id=52578297')
    assert get_res.status_code == 200


def test_scrape_author(client):
    res = client.post('/scrape/author?attr=3354.HarukiMurakami')
    assert res.status_code == 200
    get_res = client.get('/author?id=3354')
    assert get_res.status_code == 200


def test_delete_book(client):
    res1 = client.delete('/book?id=1420')
    assert res1.status_code == 200

    res2 = client.delete('/book?id=kkkkk')
    assert res2.status_code == 404


def test_delete_author(client):
    res1 = client.delete('/author?id=903')
    assert res1.status_code == 200

    res2 = client.delete('/author?id=kkkkk')
    assert res2.status_code == 404
