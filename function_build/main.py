#!/usr/bin/env python3

import functions_framework

# This file contains all the code used in the codelab.
# import sqlalchemy
# from sqlalchemy.ext.declarative import declarative_base
from google.cloud import firestore

# Add a new document
import os
import urllib
import requests

from uiuc_apartments import AllAgencies

import json


def to_json(apartment, lat, long):
    data = apartment.__dict__
    data['latitude'] = lat
    data['longitude'] = long
    return json.dumps(data)

db = firestore.Client()
doc_ref = db.collection(u'apartments').document(u'current')

def get_long_lat(address):
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
    # Get all new Apartments
    all_agencies = AllAgencies
    all_apartments = []
    for agency in all_agencies:
        all_apartments.extend(agency.get_all())


    try:
        id = 0
        doc = {}
        # Insert all Apartments
        for apt in all_apartments:
            long, lat = get_long_lat(apt.address)
            doc[str(id)] = to_json(apt, long, lat)
            id += 1
        # commit to deployment
        doc_ref.set(doc)        
    except Exception as e:
        return 'Error: {}'.format(str(e))

    return 'ok'
    
@functions_framework.http
def build_apartments(request):
    return insert_apartment(request)
