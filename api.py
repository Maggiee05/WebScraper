from flask import Flask, request, jsonify, json, make_response

import setup
from ScrapeAuthors import scrape_author
from ScrapeBooks import scrape_book
from db import get_db

# from queryInterpreter import query_interpreter
from queryInterpreter import query_interpreter

app = Flask(__name__)

myclient = get_db()[2]  # Getting the database
db = myclient["GoodReads"]


@app.route('/', methods=['GET'])
def home_page():
    return "GoodReads API home page"


@app.route('/book', methods=['GET'])
def get_book():
    if list(request.args.keys())[0] != 'id':
        return "Bad request. Please enter a book_id", 400

    book_id = request.args['id']
    book_info = db.books.find({"book_id": str(book_id)}, {"_id": 0})
    book_info_cur = list(book_info)
    if len(book_info_cur) != 0:
        return json.dumps(book_info_cur, indent=4), 200
    else:
        return "Book id Not Found. Please enter a valid id.", 404


@app.route('/author', methods=['GET'])
def get_author():
    if list(request.args.keys())[0] != 'id':
        return "Bad request. Please enter an author_id", 400

    author_id = request.args['id']
    author_info = db.authors.find({"author_id": str(author_id)}, {"_id": 0})
    author_info_cur = list(author_info)
    if len(author_info_cur) != 0:
        return json.dumps(author_info_cur, indent=4), 200
    else:
        return "author_id Not Found. Please enter a valid id.", 404


@app.route('/search', methods=['GET'])
def search_query():
    query_str = request.args['q']
    data = query_interpreter(query_str, db)
    data_cur = list(data)
    if len(data_cur) != 0:
        return json.dumps(data_cur, indent=4), 200
    else:
        return "No valid data found in database", 404


@app.route('/book', methods=['PUT'])
def put_book():
    book_id = request.args['id']
    if book_id is None:
        return "Bad request. Please enter a book_id", 400

    if db.books.count_documents({"book_id": str(book_id)}) == 0:
        return "book_id Not Found", 404

    book_info = request.get_json()
    db.books.update_one({"book_id": str(book_id)}, {"$set": book_info})
    # returning the updated info
    updated_book_info = db.books.find({"book_id": str(book_id)}, {"_id": 0})
    updated_cur = list(updated_book_info)
    return json.dumps(updated_cur, indent=4), 200


@app.route('/author', methods=['PUT'])
def put_author():
    author_id = request.args['id']
    if author_id is None:
        return "Bad request. Please enter an author_id", 400

    if db.authors.count_documents({"author_id": str(author_id)}) == 0:
        return "author_id Not Found", 404

    author_info = request.get_json()
    db.authors.update_one({"author_id": str(author_id)}, {"$set": author_info})
    # returning the updated info
    updated_author_info = db.authors.find({"author_id": str(author_id)}, {"_id": 0})
    updated_cur = list(updated_author_info)
    return json.dumps(updated_cur, indent=4), 200


@app.route('/book', methods=['POST'])
def post_book():
    book_info = request.get_json()
    if (len(book_info) != 1) or (book_info is None):
        return "Bad request.Please enter only one valid book information", 400

    else:
        db.books.insert_one(book_info[0])
        return "Successfully added one book.", 201


@app.route('/books', methods=['POST'])
def post_books():
    books_info = request.get_json()
    if (len(books_info) <= 1) or (books_info is None):
        return "Bad request.Please enter several valid books information", 400

    else:
        for item in books_info:
            db.books.insert_one(item)
        return "Successfully added several books.", 201


@app.route('/author', methods=['POST'])
def post_author():
    author_info = request.get_json()
    if (len(author_info) != 1) or (author_info is None):
        return "Bad request.Please enter only one valid author information", 400

    else:
        db.authors.insert_one(author_info[0])
        return "Successfully added one author.", 201


@app.route('/authors', methods=['POST'])
def post_authors():
    authors_info = request.get_json()
    if (len(authors_info) <= 1) or (authors_info is None):
        return "Bad request.Please enter several valid authors information", 400

    else:
        for item in authors_info:
            db.authors.insert_one(item)
        return "Successfully added several authors.", 201


@app.route('/scrape/book', methods=['POST'])
def post_scrape_book():
    """ Specify the book id to scrape a book"""

    book_id = request.args['id']
    url_book = "https://www.goodreads.com/book/show/" + book_id
    setup.books_list.append({"book_url": url_book})
    book_data = scrape_book(0)
    if db.books.count_documents(book_data) == 0:
        db.books.insert_one(book_data)
    return "Successfully scrape one book", 200


@app.route('/scrape/author', methods=['POST'])
def post_scrape_author():
    """
    Specify the attr with author id and name to scrape a book
    Connect with '.'. For example, 12345.Jason
    """

    author_info = request.args['attr']
    author_name = author_info.split('.')[1]
    url_author = "https://www.goodreads.com/book/show/" + author_info
    setup.authors_list.append({"name": author_name, "author_url": url_author})
    author_data = scrape_author(0)
    if db.authors.count_documents(author_data) == 0:
        db.authors.insert_one(author_data)
    return "Successfully scrape one author", 200


@app.route('/book', methods=['DELETE'])
def delete_book():
    """ Delete book specified by the ID """
    book_id = request.args['id']
    if db.books.count_documents({"book_id": str(book_id)}) != 0:
        db.books.delete_one({"book_id": str(book_id)})
        return "Successfully deleted", 200
    else:
        return "book_id Not Found. Cannot be deleted", 404


@app.route('/author', methods=['DELETE'])
def delete_author():
    """ Delete author specified by the ID """
    author_id = request.args['id']
    if db.authors.count_documents({"author_id": str(author_id)}) != 0:
        db.authors.delete_one({"author_id": str(author_id)})
        return "Successfully deleted", 200
    else:
        return "author_id Not Found. Cannot be deleted", 404


if __name__ == '__main__':
    app.run(debug=True)
