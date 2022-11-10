import functions_framework
import datetime

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
class Apartments(Base):
    __tablename__ = 'apartments'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    address = sqlalchemy.Column(sqlalchemy.String)
    rent = sqlalchemy.Column(sqlalchemy.Float)
    bedrooms = sqlalchemy.Column(sqlalchemy.Integer)
    bathrooms = sqlalchemy.Column(sqlalchemy.Float)
    link = sqlalchemy.Column(sqlalchemy.String)
    available_date = sqlalchemy.Column(sqlalchemy.String)
    agency = sqlalchemy.Column(sqlalchemy.String)
    is_studio = sqlalchemy.Column(sqlalchemy.Boolean)
  
@functions_framework.http
def get_apartments(request):
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
      session = sqlalchemy.orm.Session(db)
      # get apartments with agency in request
      apartments = session.query(Apartments).filter(Apartments.agency == request.args.get('agency')).all()
      # convert apartments to json
      apartments_json = [apartment.__dict__ for apartment in apartments]
      return apartments_json
  except Exception as e:
      print(e)
      return "Error"