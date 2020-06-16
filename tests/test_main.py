import unittest


class MainTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_true(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
