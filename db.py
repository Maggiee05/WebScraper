import json
import sys

from pymongo import MongoClient
import os
from dotenv import load_dotenv
import setup


def get_db():
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY")
    myclient = MongoClient(SECRET_KEY)
    mydb = myclient["GoodReads"]
    authors_info = mydb.authors
    books_info = mydb.books

    # record = {"name": "J.K. Rowling",
    #           "author_url": "https://www.goodreads.com/author/show/1077326.J_K_Rowling"}
    #
    # authors_info.insert_one(record)

    return authors_info, books_info, myclient


def export_json(collection, file):
    cursor = collection.find({}, {"_id": False})
    list_cur = list(cursor)
    json_data = json.dumps(list_cur, indent=4)
    with open(file, "w") as f:
        f.write(json_data)
    print("Successfully write into json file")
    f.close()

    get_db()[2].close()


def import_json(collection, file):
    with open(file) as f:
        data = json.load(f)
        if isinstance(data, list):
            collection.insert_many(data)
            print("Successfully insert into authors database")
        else:
            collection.insert_one(data)
    f.close()

    get_db()[2].close()
