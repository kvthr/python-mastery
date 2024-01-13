from stock import Stock
import unittest

class TestStock(unittest.TestCase):
    def test_create(self):
        s = Stock("GG", 90, 9090.9)
        self.assertEqual(s.name, 'GG')
        self.assertEqual(s.shares, 90)
        self.assertEqual(s.price, 9090.9)

    def test_cost(self):
        s = Stock("GG", 90, 9090.9)
        self.assertEqual(s.cost, 90 * 9090.9)

    def test_sell(self):
        s = Stock("GG", 90, 9090.9)

        s.sell(5)
        self.assertEqual(s.shares, 85)

    def test_from_row(self):
        s = Stock.from_row(["GG", 90, 9090.9])
        self.assertEqual(s.name, 'GG')
        self.assertEqual(s.shares, 90)
        self.assertEqual(s.price, 9090.9)

    def test_repr(self):
        s = Stock.from_row(["GG", 90, 9090.9])
        self.assertEqual(repr(s), "Stock('GG', 90, 9090.9)")

    def test_equal(self):

        a = Stock("GG", 90, 9090.9)
        b = Stock("GG", 90, 9090.9)
        self.assertEqual(a, b)

    def test_bad_shares(self):
        s = Stock.from_row(["GG", 90, 9090.9])
        with self.assertRaises(TypeError):
            s.shares = "60"

        with self.assertRaises(ValueError):
            s.shares = -90

    def test_bad_price(self):
        s = Stock.from_row(["GG", 90, 9090.9])
        with self.assertRaises(TypeError):
            s.price = "60.60"

        with self.assertRaises(ValueError):
            s.price = -90.90

    def test_attribute(self):
        s = Stock.from_row(["GG", 90, 9090.9])
        with self.assertRaises(AttributeError):
            s.share = 60

if __name__=="__main__":
    unittest.main()