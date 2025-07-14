import unittest

class TestHelloWorld(unittest.TestCase):
    def test_hello(self):
        self.assertEqual('hello world', 'hello world')

if __name__ == '__main__':
    unittest.main()
