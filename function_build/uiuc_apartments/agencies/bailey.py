import requests
from bs4 import BeautifulSoup
from uiuc_apartments.shared import AgencyBase, Apartment

class Bailey(AgencyBase):
    url = 'https://baileyapartments.com/amenities/'
    name = "Bailey Apartments"

    def get_all(self):
        apartments = []
        res = requests.get(self.url).text
        soup = BeautifulSoup(res, 'html.parser')
        # Get each row in the table with class="tablepress-2", using thead as dictionary keys
        table = soup.find('table', id='tablepress-2')
        thead = table.find('thead')
        keys = [th.text.strip() for th in thead.find_all('th')]
        for tr in table.find('tbody').find_all('tr'):
            lookup = {}
            for i, td in enumerate(tr.find_all('td')):
                lookup[keys[i]] = td.text.strip()
            address = lookup['Building']
            # normalize the address into a url slug
            slug = address.lower().replace(' ', '-').replace('.', '').replace(',', '')
            if lookup['# of Bedrooms'] != 'Efficiency':
                bedrooms = int(lookup['# of Bedrooms'])
                is_studio = False
            else:
                bedrooms = 1
                is_studio = True
            bathrooms = float(lookup['# of Baths'])
            price = float(lookup['Price (per month)'].split(
                ' - ')[-1].replace('$', '').replace(',', ''))
            link = 'https://baileyapartments.com/apartment/' + slug
            available_date = '2023-08-01' if lookup['Availability (AVAILABLE 2023-2024)'] == 'Available' else None
            apartments.append(Apartment(address, price, bedrooms,
                                        bathrooms, link, available_date, self.name, is_studio))
        return apartments