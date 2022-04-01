import inspect
from azure_sql_util import azure_sql_util

if inspect.isclass(azure_sql_util):
    azure_sql_util().main()
else:
    azure_sql_util.azure_sql_util().main()
