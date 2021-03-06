"""Unit testing"""
import unittest

import ScrapeBooks
import setup
import ScrapeAuthors


class TestStringMethods(unittest.TestCase):
    """
    Class holding all the test cases
    """

    def test_author_traversal(self):
        """
        Test case for author_traversal
        Check if the traversal of the authors won't duplicate, and is successfully traversed
        """
        ScrapeAuthors.author_traversal("J.K. Rowling",
                                       "https://www.goodreads.com/author/show/1077326.J_K_Rowling")
        ScrapeAuthors.author_traversal("Stephenie Meyer",
                                       "https://www.goodreads.com/author/show/941441.Stephenie_Meyer")
        ScrapeAuthors.author_traversal("John Green",
                                       "https://www.goodreads.com/author/show/1406384.John_Green")
        # should insert 3 new author by now
        self.assertEqual(len(setup.authors_list), 3)

        ScrapeAuthors.author_traversal("John Green",
                                       "https://www.goodreads.com/author/show/1406384.John_Green")
        # should still be 3 since duplicated
        self.assertEqual(len(setup.authors_list), 3)

    def test_book_traversal(self):
        """
        Test case for book_traversal
        Check if the traversal of the books won't duplicate, and is successfully traversed
        """
        ScrapeBooks.book_traversal(
            "https://www.goodreads.com/book/show/2767052-the-hunger-games")
        ScrapeBooks.book_traversal(
            "https://www.goodreads.com/book/show/11870085-the-fault-in-our-stars")
        # should insert 2 new books by now
        self.assertEqual(len(setup.books_list), 2)

        ScrapeBooks.book_traversal(
            "https://www.goodreads.com/book/show/11870085-the-fault-in-our-stars")
        # should still be 2 since duplicated
        self.assertEqual(len(setup.books_list), 2)

    def test_scrape_author(self):
        test_author = {"name": "Haruki Murakami",
                       "author_url": "https://www.goodreads.com/author/show/3354.HarukiMurakami"}
        setup.authors_list.append(test_author)
        res = ScrapeAuthors.scrape_author(0)
        res["author_id"] = "3354"

    def test_scrape_book(self):
        test_book = {"book_url": "https://www.goodreads.com/book/show/11297.Norwegian_Wood"}
        setup.books_list.append(test_book)
        res = ScrapeBooks.scrape_book(0)
        res["title"] = "Norwegian Wood"


if __name__ == '__main__':
    unittest.main()
