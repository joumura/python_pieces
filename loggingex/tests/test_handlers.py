import unittest
from unittest.mock import MagicMock
from loggingex.handlers import MyTimedRotatingFileHandler


class TestMyTimedRotatingFileHandler(unittest.TestCase):

    def test_shouldRollover(self):
        handler = MyTimedRotatingFileHandler('myapp.log', 'd', 'utf-8')
        handler.baseFilename = \
            handler._MyTimedRotatingFileHandler__make_logfilename()
        true_or_false = handler.shouldRollover(None)
        self.assertFalse(true_or_false)
        handler.baseFilename = 'myapp.log'
        true_or_false = handler.shouldRollover(None)
        self.assertTrue(true_or_false)

    def test_doRollover(self):
        handler = MyTimedRotatingFileHandler('myapp.log', 'd', 'utf-8')
        handler.stream = None
        handler.doRollover()
        self.assertIsNotNone(handler.stream)

    def test_doRollover_delay(self):
        handler = MyTimedRotatingFileHandler('myapp.log', 'd', 'utf-8')
        handler.delay = True
        strm_mock = MagicMock()
        handler.stream = strm_mock
        handler.doRollover()
        strm_mock.close.assert_called_once_with()
        self.assertIsNone(handler.stream)

    def test___make_logfilename(self):
        handler = MyTimedRotatingFileHandler('myapp.log', 'd', 'utf-8')
        logfilename = handler._MyTimedRotatingFileHandler__make_logfilename()
        print(f'logfilename: {logfilename}')
        self.assertRegex(logfilename, 'myapp\\.[0-9]{8}\\.log')


# if __name__ == "__main__":
#     unittest.main()
