""" Unit test for query operator"""
import unittest

from queryInterpreter import dot_operator, quote_operator, \
    logical_operator, comparison_operator, parse_expression


class TestQuery(unittest.TestCase):

    def test_parse_expression(self):
        expr1 = '>1200'
        attr1 = 'review_count'
        self.assertEqual({"$gt": 1200.0}, parse_expression(attr1, expr1))
        expr2 = '"4.92"'
        attr2 = 'rating'
        self.assertEqual(4.92, parse_expression(attr2, expr2))

    def test_dot_operator(self):
        expression = 'book.rating_count'
        self.assertEqual('book', dot_operator(expression)[0])
        self.assertEqual('rating_count', dot_operator(expression)[1])

    def test_quote_operator(self):
        expression1 = 'aaa"12456"bbb'
        expression2 = 'aaa"121bb'
        expression3 = '"123"'
        self.assertEqual('12456', quote_operator(expression1))
        self.assertEqual(('Bad request. Quotes not enclose correctly', 400),
                         quote_operator(expression2))
        self.assertEqual('123', quote_operator(expression3))

    def test_logical_operator(self):
        expression1 = '>123 AND <500'
        expression2 = '12 OR <200'
        expression3 = 'NOT >2000'
        self.assertEqual('$and', logical_operator(expression1)[0])
        self.assertEqual(['>123', '<500'], logical_operator(expression1)[1])
        self.assertEqual('$or', logical_operator(expression2)[0])
        self.assertEqual(['12', '<200'], logical_operator(expression2)[1])
        self.assertEqual(['>2000'], logical_operator(expression3)[1])

    def test_comparison_operator(self):
        expression1 = '< nooo'
        expression2 = '>200'
        expression3 = '<4.67'
        self.assertEqual(("Bad request. Please enter a valid number to compare", 400),
                         comparison_operator(expression1))
        self.assertEqual({'$gt': 200.0}, comparison_operator(expression2))
        self.assertEqual({'$lt': 4.67}, comparison_operator(expression3))


if __name__ == '__main__':
    unittest.main()
