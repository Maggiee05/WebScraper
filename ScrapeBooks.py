"""
Scraping for books
Have attributes:
book_url, title, book_id, ISBN, author_url, author, rating, rating_count, review_count, image_url, similar_books
The traversal order is visiting similar books listed in the GoodReads website.
"""

import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup

import setup
import re


def get_title_book(soup):
    title = soup.find("h1", id="bookTitle").text.strip()
    return title


def get_id_book(url):
    path = url.split("/")[-1]
    book_id = re.search("[0-9]+", path).group()
    return book_id


def get_isbn_book(soup):
    isbn = soup.find("meta", property="books:isbn")["content"]
    if isbn == "null":
        print("This book does not have ISBN")

    return isbn


def get_author_url_book(soup):
    urls = []
    all_authors = soup.find_all("a", class_="authorName")
    for author in all_authors:
        urls.append(author["href"].strip())

    return urls


def get_author_book(soup):
    authors = []
    all_authors = soup.find_all("span", itemprop="name")
    for author in all_authors:
        authors.append(author.text)

    return authors


def get_rating_book(soup):
    rating = soup.find("span", itemprop="ratingValue").text.strip()
    return rating


def get_rating_count_book(soup):
    rating_count = soup.find("meta", itemprop="ratingCount")["content"].strip()
    return rating_count


def get_review_count_book(soup):
    review_count = soup.find("meta", itemprop="reviewCount")["content"].strip()
    return review_count


def get_image_url_book(soup):
    image_url = soup.find("img", id="coverImage")["src"]
    return image_url


def get_similar_books(soup):
    similar_books = []
    all_books = soup.find("div", id=re.compile("^relatedWorks-"))
    all_books_info = all_books.find_all("li", class_="cover")

    for book in all_books_info:
        next_url = book.find("a")["href"]
        book_traversal(next_url)
        similar_books.append(next_url)
        book_traversal(next_url)

    return similar_books


def scrape_book(idx):
    book = setup.books_list[idx]
    try:
        url = book["book_url"]
        source = urlopen(url)
        soup = BeautifulSoup(source, "html.parser")
    except:
        # if the url provided is not valid, error message generated and exit the program
        sys.exit("Book URL not valid")

    book["title"] = get_title_book(soup)
    book["book_id"] = get_id_book(url)
    book["ISBN"] = get_isbn_book(soup)

    book["author_url"] = get_author_url_book(soup)
    book["author"] = get_author_book(soup)
    book["rating"] = get_rating_book(soup)
    book["rating_count"] = get_rating_count_book(soup)
    book["review_count"] = get_review_count_book(soup)
    book["image_url"] = get_image_url_book(soup)
    book["similar_books"] = get_similar_books(soup)
    print("Current book%d done. Moving to the next book........" % idx)

    return book


def book_traversal(next_url):
    if not any(book["book_url"] == next_url for book in setup.books_list):
        next_book = {"book_url": next_url}
        setup.books_list.append(next_book)
