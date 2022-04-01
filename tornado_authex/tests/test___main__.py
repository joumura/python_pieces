import unittest
# from unittest.mock import MagicMock
from tornado_authex.__main__ import main


class Test__main__(unittest.TestCase):

    def test___main__(self):
        main()
