import unittest


class MainTestCase(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_true(self):
        self.assertTrue(True)


class YandexBucketTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        import warnings
        from uuid import uuid1
        from main import YandexCloudS3
        warnings.simplefilter("ignore")
        cls.key_test = str(uuid1())
        cls.body_test = str(uuid1())
        cls.yc = YandexCloudS3()

    def test_01_write_file(self):
        self.result = self.yc.upload(self.key_test, self.body_test)
        self.assertTrue(type(self.result) == dict)

    def test_02_read_file(self):
        self.result = self.yc.download(self.key_test)
        self.body_result = str(self.result.get('Body').read().decode("utf-8"))
        self.assertTrue(self.body_test == self.body_result)

    def test_03_delete_file(self):
        self.result = self.yc.delete(self.key_test)
        self.assertTrue(type(self.result) == dict)


if __name__ == '__main__':
    unittest.main()
