#!/usr/bin/env python3

import functions_framework

# This file contains all the code used in the codelab.
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

import os
import urllib
import requests

from uiuc_apartments import AllAgencies

connection_name = "champaign-apartment-aggregator:us-central1:champaign-apartment-postgresql"
table_name = "apartments"
db_name = "postgres"
db_user = "postgres"
db_password = "postgres"

# If your database is PostgreSQL, uncomment the following two lines:
driver_name = 'postgresql+pg8000'

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
    latitude = sqlalchemy.Column(sqlalchemy.Float)
    longitude = sqlalchemy.Column(sqlalchemy.Float)

def get_lat_long(address):
    API_KEY = os.environ.get("API_KEY", "XXXX")
    uiuc_min_long = -88.5
    uiuc_max_long = -88
    uiuc_min_lat = 40
    uiuc_max_lat = 40.3
    uiuc_center_long = -88.2
    uiuc_center_lat = 40.1
    address = urllib.parse.quote(address)
    request_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json?country=us&bbox=\
{uiuc_min_long},{uiuc_max_long},{uiuc_min_lat},{uiuc_max_lat}&proximity={uiuc_center_long},{uiuc_center_lat}&limit=1&types=address&autocomplete=false&\
fuzzyMatch=true&routing=false&worldview=us&access_token={API_KEY}"
    response = requests.get(request_url)
    if response.status_code != 200:
        return (0, 0)
    response = response.json()
    if 'features' in response and len(response['features']) > 0:
        return response['features'][0]['center']
    # TODO: could not find the address, so don't commit it to database?
    return (0, 0) 

def insert_apartment(_):
    db = sqlalchemy.create_engine(
      sqlalchemy.engine.url.URL(
        drivername=driver_name,
        username=db_user,
        password=db_password,
        database=db_name,
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
            lat, long = get_lat_long(apt.address)
            apartment = Apartments(address=apt.address, rent=apt.rent, bedrooms=apt.bedrooms, bathrooms=apt.bathrooms,
                link=apt.link, available_date=apt.available_date, agency=apt.agency, is_studio=apt.is_studio,
                latitude=lat, longitude=long)
            session.add(apartment)
        
        # Commit Changes
        session.commit()
    except Exception as e:
        return 'Error: {}'.format(str(e))

    return 'ok'

@functions_framework.http
def build_apartments(request):
    return insert_apartment(request)
