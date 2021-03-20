"""
Scraping for authors
Have attributes:
name, author_url, author_id, rating, rating_count, review_count, image_url, related_authors, author_books
The traversal order is visiting the related authors listed in the GoodReads website.
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup

from src import setup
import re

setup.authors_list = []


def get_name_author(soup):
    name = soup.find("meta", property="og:title")["content"]
    return name


def get_id_author(url):
    path = url.split("/")[-1]
    author_id = re.search("[0-9]+", path).group()
    return author_id


def get_rating_author(soup):
    ratings = soup.find("span", itemprop="ratingValue").text.strip()
    return float(ratings)


def get_rating_count_author(soup):
    count = soup.find("span", itemprop="ratingCount")["content"].strip()
    print(count)
    return int(count)


def get_review_count_author(soup):
    count = soup.find("span", itemprop="reviewCount")["content"].strip()
    return int(count)


def get_image_url_author(soup, name):
    image_url = soup.find("img", alt=name)["src"]
    return image_url


def get_related_authors(soup):
    related_authors = []
    path = soup.find("a", text="Similar authors")["href"]
    url = "https://goodreads.com" + path
    source = urlopen(url)
    authors_soup = BeautifulSoup(source, "html.parser")
    authors_tags = authors_soup.find_all("span", itemprop="name")

    for i in range(1, len(authors_tags)):  # the 0 index is the current author
        next_name = authors_tags[i].text
        next_url = authors_tags[i].parent["href"]
        author_traversal(next_name, next_url)
        related_authors.append(next_url)

    return related_authors


def get_author_books(soup):
    author_books = []
    all_books = soup.find_all("tr", itemtype="http://schema.org/Book")
    for book in all_books:
        path = book.find("a", class_="bookTitle")["href"]
        url = "https://goodreads.com" + path
        author_books.append(url)

    return author_books


def scrape_author(idx):
    author = setup.authors_list[idx]
    url = author["author_url"]
    source = urlopen(url)
    soup = BeautifulSoup(source, "html.parser")

    # author["name"] = get_name_author(soup)
    author["author_id"] = get_id_author(url)
    author["rating"] = get_rating_author(soup)
    author["rating_count"] = get_rating_count_author(soup)
    author["review_count"] = get_review_count_author(soup)
    author["image_url"] = get_image_url_author(soup, author["name"])
    author["related_authors"] = get_related_authors(soup)
    author["author_books"] = get_author_books(soup)
    print("Current author%d done. Moving to the next author........" % idx)

    return author


def author_traversal(next_name, next_url):
    if not any(author["name"] == next_name for author in setup.authors_list):
        next_author = {"name": next_name}
        setup.authors_list.append(next_author)
        next_author["author_url"] = next_url
