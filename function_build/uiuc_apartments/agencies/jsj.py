import requests
import json
from bs4 import BeautifulSoup
from uiuc_apartments.shared import AgencyBase, Apartment

class JSJ(AgencyBase):
    url = 'https://jsjmanagement.com/on-campus'
    name = "JSJ Management"

    def get_all(self):
        apartments = []
        res = requests.get(self.url).text
        soup = BeautifulSoup(res, 'html.parser')
        # Get script with type="application/json" and id="search-form-config"
        script = soup.find('script', type='application/json',
                           id='search-form-config').text
        data = json.loads(script)
        for apartment in data['properties']['data']:
            bedrooms = int(apartment['bedrooms'])
            if bedrooms == 0:
                bedrooms = 1
                is_studio = True
            else:
                is_studio = False
            bathrooms = float(apartment['bathrooms'])
            address = apartment['address_1']
            link = 'https://jsjmanagement.com/on-campus/listing/' + \
                apartment['slug']
            price = float(apartment['price'].replace(',', ''))
            avail_date = apartment['avail_date']
            # If avail_date is later than 08-01-2023, then available
            apartments.append(Apartment(address, price, bedrooms,
                                        bathrooms, link, avail_date, self.name, is_studio))
        return apartments