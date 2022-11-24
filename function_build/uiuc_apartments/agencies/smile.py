import requests
from uiuc_apartments.shared import AgencyBase, Apartment
import json

class Smile(AgencyBase):
    url = 'https://www.smilestudentliving.com/_dm/s/rt/actions/sites/24eaedf2/collections/appfolio-listings/ENGLISH'
    name = "Smile"

    def get_all(self):
        apartments = []
        # request with user agent

        contents = requests.get(
            self.url, headers={'User-Agent': 'api-scraper'}).json()
        apartment_list = json.loads(contents['value'])
        for apartment in apartment_list:
            details = apartment['data']
            address = details['address_address1']
            available_date = details.get('available_date', None)
            bathrooms = details['bathrooms']
            bedrooms = details['bedrooms']
            # Studio
            is_studio = False
            if bedrooms == 0:
                bedrooms = 1
                is_studio = True
            market_rent = int(details['market_rent'])
            # rent == 0 if sublease only
            if market_rent == 0:
                continue
            link = "https://www.smilestudentliving.com/listings/detail/" + \
                apartment['page_item_url']
            apartments.append(Apartment(address, market_rent, bedrooms,
                                        bathrooms, link, available_date, self.name, is_studio))

        return apartments