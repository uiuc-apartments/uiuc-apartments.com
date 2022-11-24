import functions_framework
from flask import jsonify
from dataclasses import dataclass
from uiuc_apartments import AllAgencies
# This file contains all the code used in the codelab.
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


connection_name = "champaign-apartment-aggregator:us-central1:champaign-apartment-postgresql"
table_name = "apartments"
db_name = "postgres"
db_user = "postgres"
db_password = "postgres"

# If your database is PostgreSQL, uncomment the following two lines:
driver_name = 'postgresql+pg8000'
query_string =  dict({"unix_sock": "/cloudsql/{}/.s.PGSQL.5432".format(connection_name)})

Base = declarative_base()
@dataclass
class Apartments(Base):
    id: int
    address: str
    rent: float
    bedrooms: int
    bathrooms: float
    link: str
    available_date: str
    agency: str
    is_studio: bool
    latitude: float
    longitude: float

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

@functions_framework.http
def get_apartments(request):

    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

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
        all_agencies = [agency.name for agency in AllAgencies]
        agencies = request.args.get('agencies')
        agencies = agencies.split(',') if agencies else all_agencies

        min_rent = request.args.get('min_rent', 0)
        max_rent = request.args.get('max_rent', 9999)

        min_bedrooms = request.args.get('min_bedrooms', 0)
        max_bedrooms = request.args.get('max_bedrooms', 9999)

        min_bathrooms = request.args.get('min_bathrooms', 0)
        max_bathrooms = request.args.get('max_bathrooms', 9999)

        earliest_available_date = request.args.get('earliest_available_date', '1900-01-01')
        latest_available_date = request.args.get('latest_available_date', '9999-12-31')

        is_studio = request.args.get('is_studio', False)

        session = sqlalchemy.orm.Session(db)
        
        # get apartments with agency in request
        query = session.query(Apartments) \
        .filter(Apartments.agency.in_(agencies)) \
        .filter(Apartments.rent >= min_rent) \
        .filter(Apartments.rent <= max_rent) \
        .filter(Apartments.bedrooms >= min_bedrooms) \
        .filter(Apartments.bedrooms <= max_bedrooms) \
        .filter(Apartments.bathrooms >= min_bathrooms) \
        .filter(Apartments.bathrooms <= max_bathrooms) \
        .filter(Apartments.is_studio == is_studio) \
        # .filter(Apartments.available_date >= earliest_available_date) \
        # .filter(Apartments.available_date <= latest_available_date)
        # convert apartments to json
        results = query.all()
        print(results[14:17])

        # Set CORS headers for the main request
        headers = {
            'Access-Control-Allow-Origin': '*'
        }
        session.close()

        return jsonify(results), 200, headers
    except Exception as e:
        print(e)
        return "Error"
