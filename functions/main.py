#!/usr/bin/env python3

import functions_framework
import datetime

# This file contains all the code used in the codelab.
import sqlalchemy

# Depending on which database you are using, you'll set some variables differently.
# In this code we are inserting only one field with one value.
# Feel free to change the insert statement as needed for your own table's requirements.

# Uncomment and set the following variables depending on your specific instance and database:
connection_name = "champaign-apartment-aggregator:us-central1:champaign-apartment-postgresql"
table_name = "testing1"
table_field = "testingtime"
#table_field_value = ""
db_name = "postgres"
db_user = "postgres"
db_password = "postgres"

# If your database is MySQL, uncomment the following two lines:
#driver_name = 'mysql+pymysql'
#query_string = dict({"unix_socket": "/cloudsql/{}".format(connection_name)})

# If your database is PostgreSQL, uncomment the following two lines:
driver_name = 'postgres+pg8000'
query_string =  dict({"unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(connection_name)})

# If the type of your table_field value is a string, surround it with double quotes.

def insert():
    table_field_value = str(datetime.datetime.now())
    stmt = sqlalchemy.text('insert into {} ({}) values ({})'.format(table_name, table_field, table_field_value))

    db = sqlalchemy.create_engine(
      sqlalchemy.engine.url.URL(
        drivername=driver_name,
        username=db_user,
        password=db_password,
        database=db_name,
        query=query_string,
      ),
      pool_size=5,
      max_overflow=2,
      pool_timeout=30,
      pool_recycle=1800
    )
    try:
        with db.connect() as conn:
            conn.execute(stmt)
    except Exception as e:
        return 'Error: {}'.format(str(e))
    return 'ok'

@functions_framework.http
def hello_get(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    Note:
        For more information on how Flask integrates with Cloud
        Functions, see the `Writing HTTP functions` page.
        <https://cloud.google.com/functions/docs/writing/http#http_frameworks>
    """
    return insert()
