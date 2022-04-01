import unittest
# from unittest.mock import MagicMock
from azure_sql_util import azure_sql_util


class TestAzure_sql_util(unittest.TestCase):

    def test_main(self):
        azure_sql_util.azure_sql_util().main()
