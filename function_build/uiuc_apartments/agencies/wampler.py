import requests
from bs4 import BeautifulSoup
from uiuc_apartments.shared import AgencyBase, Apartment

class Wampler(AgencyBase):
    url = 'https://wamplerapartments.com/?availability=august'
    name = "Wampler Apartments"

    def get_all(self):
        apartments = []
        # Get all links with class="more-link"
        res = requests.get(self.url).text
        soup = BeautifulSoup(res, 'html.parser')
        for a in soup.find_all('a', class_='more-link'):
            # Get soup
            link = a['href']
            res = requests.get(link).text
            soup = BeautifulSoup(res, 'html.parser')
            # Get h3 with class="listing-address"
            address = soup.find('h3', class_='listing-address').text.strip()
            lookup = {}
            # Get all div with class="single-detail" with the key as span class="label" and value as span class="value"
            for div in soup.find_all('div', class_='single-detail'):
                spans = div.find_all('span')
                lookup[spans[0].text.strip()] = spans[1].text.strip()
            if lookup['Bedrooms:'] == 'Studio':
                bedrooms = 1
                is_studio = True
            else:
                bedrooms = int(lookup['Bedrooms:'])
                is_studio = False
            bathrooms = float(lookup['Bathrooms:'])
            available = lookup['Rent:'].upper() != 'LEASED'
            if available:
                available_date = '2023-08-01'
                price = float(lookup['Rent:'].replace(
                    '$', '').replace(',', ''))
            else:
                available_date = None
                price = 0
            apartments.append(Apartment(address, price, bedrooms,
                                        bathrooms, link, available_date, self.name, is_studio))
        return apartments