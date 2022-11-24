import requests
from bs4 import BeautifulSoup
from uiuc_apartments.shared import AgencyBase, Apartment
import re

class MHM(AgencyBase):
    url = "https://www.mhmproperties.com/apartments/?_sft_types=apartments"
    name = "MHM"

    def get_all(self):
        apartments = []
        page = requests.get(self.url, headers={
                            'User-Agent': 'api-scraper'}).text
        soup = BeautifulSoup(page, 'html.parser')
        # print(page)
        # Get all divs with class="propgridc"
        locations = soup.find_all('div', class_='propgridc')
        # Loop through each location
        for location in locations:
            # Get the link
            link = location.find('a')['href']
            # Get the address as the h2 tag
            address = location.find('h2').text
            # Get all p tags with class="ppricebox"
            ps = location.find_all('p', class_='ppricebox')
            for p in ps:
                # print(p.text)
                # A regex to capture the word optional word bath followed by a number
                regex = re.compile(
                    r'(?P<bed>\d+) Bed(?:\/(?P<bath>[\d\.]+) Bath)?.*:(?:.*\$(?P<rent>\d+,?\d+)\W{1,2}?(?P<kind>\w+)|.*(?P<available>LEASED!))')
                # Use regex against p tag
                match = regex.search(p.text)
                # If there is a match
                if match:
                    # Get the number of bedrooms
                    bedrooms = int(match.group('bed'))
                    # Get the number of bathrooms
                    bathrooms = float(match.group('bath') or 1)
                    # Get the rent
                    rent = match.group('rent')
                    if rent:
                        rent = int(rent.replace(',', ''))
                    else:
                        # If rent is not found, apartment is leased (or something is broken)
                        continue
                    # Get the kind of unit
                    kind = match.group('kind')
                    if kind == 'person':
                        rent *= bedrooms
                    # Get the availability
                    availabile = match.group('available') != 'LEASED!'
                    if availabile:
                        available_date = '2023-08-01'
                    else:
                        available_date = None

                    is_studio = False
                    # Add an apartment to the list
                    apartments.append(Apartment(
                        address, rent, bedrooms, bathrooms, link, available_date, self.name, is_studio))

        return apartments