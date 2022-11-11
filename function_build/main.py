#!/usr/bin/env python3

import functions_framework
import datetime

# This file contains all the code used in the codelab.
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

from api import AllAgencies

connection_name = "champaign-apartment-aggregator:us-central1:champaign-apartment-postgresql"
table_name = "apartments"
db_name = "postgres"
db_user = "postgres"
db_password = "postgres"

# If your database is PostgreSQL, uncomment the following two lines:
driver_name = 'postgresql+pg8000'
query_string =  dict({"unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(connection_name)})

Base = declarative_base()
class Apartments(Base):
    __tablename__ = 'apartments'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    address = sqlalchemy.Column(sqlalchemy.String)
    rent = sqlalchemy.Column(sqlalchemy.Float)
    bedrooms = sqlalchemy.Column(sqlalchemy.Integer)
    bathrooms = sqlalchemy.Column(sqlalchemy.Float)
    link = sqlalchemy.Column(sqlalchemy.String)
    available_date = sqlalchemy.Column(sqlalchemy.Date)
    agency = sqlalchemy.Column(sqlalchemy.String)
    is_studio = sqlalchemy.Column(sqlalchemy.Boolean)

def insert_apartment(request):
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
    # Create table is not exists
    Base.metadata.create_all(db, checkfirst=True)

    # Get all new Apartments
    all_agencies = AllAgencies
    all_apartments = []
    for agency in all_agencies:
        all_apartments.extend(agency.get_all())


    try:
        session = sqlalchemy.orm.Session(db)

        # Delete all Apartments
        session.query(Apartments).delete()

        # Insert all Apartments
        for apt in all_apartments:
            apartment = Apartments(address=apt.address, rent=apt.rent, bedrooms=apt.bedrooms, bathrooms=apt.bathrooms, link=apt.link, available_date=apt.available_date, agency=apt.agency, is_studio=apt.is_studio)
            session.add(apartment)
        
        # Commit Changes
        session.commit()
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
    return insert_apartment(request)
