azure-sql-util
==========

Operation tools needed when using Azure SQL.


azure_sql_util
==========
GUI that helps the following procedures when using Azure SQL.
1. Change login password
2. (For administrators) Add login & user
3. (For administrators) Delete login & user

Usage
-----

The GUI starts with the following command.
```
py -m azure_sql_util
```
If you really want to use it, it would be better to make it into an exe with pyinstaller for the environment where python is not installed.

----

copy_tables
==========

If you want to backup Azure SQL data, creating another DB will increase the billing amount. So a tool for replicating to another schema.

Usage
-----

The following command can list the table to be backed up and the number of rows.
```
py -m azure_sql_util.copy_table
```
Duplicate the table to {schema name} with the following command.
```
py -m azure_sql_util.copy_table {schema name}
```
