import argparse
import sys

from ScrapeBooks import scrape_book
from ScrapeAuthors import scrape_author
import setup
from db import export_json, get_db, import_json


def main():
    inputs = command_line()

    book_number = inputs.book_num
    author_number = inputs.author_num
    if book_number > 200:
        sys.exit("Invalid input. Please enter a book number < 200")
    if author_number > 50:
        sys.exit("Invalid input. Please enter an author number < 50")

    # starting point for scraping
    start_url = inputs.starting_url
    setup.books_list.append({"book_url": start_url})

    book_collection = get_db()[1]
    author_collection = get_db()[0]
    for i in range(book_number):
        book_data = scrape_book(i)
        if book_collection.count_documents(book_data) == 0:
            book_collection.insert_one(book_data)

    start_book = setup.books_list[0]
    setup.authors_list.append({"name": start_book["author"][0], "author_url": start_book["author_url"][0]})

    for j in range(author_number):
        author_data = scrape_author(j)
        if author_collection.count_documents(author_data) == 0:
            author_collection.insert_one(author_data)

    if inputs.export:
        export_json(author_collection, "authors.json")
        export_json(book_collection, "books.json")

    if inputs.update:
        import_json(author_collection, "authors.json")
        import_json(book_collection, "books.json")


def command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument("starting_url", type=str, help="Starting url for the scraping")
    parser.add_argument("book_num", type=int, help="Number of books to scrape")
    parser.add_argument("author_num", type=int, help="Number of authors to scrape")
    parser.add_argument("--export", help="Export json file from database")
    parser.add_argument("--update", help="Insert/Update json file into database")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
