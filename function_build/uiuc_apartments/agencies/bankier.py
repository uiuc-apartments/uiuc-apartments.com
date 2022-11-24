import requests
from bs4 import BeautifulSoup
from uiuc_apartments.shared import AgencyBase, Apartment
import re

class Bankier(AgencyBase):
    url = 'https://www.bankierapartments.com/apartments/'
    name = "Bankier Properties"

    def get_all(self):
        res = requests.get(self.url).text
        soup = BeautifulSoup(res, 'html.parser')
        # Get all a tags with the title="View Property Units"
        apartments = []
        for a in soup.find_all('a', title='View Property Units'):
            # Get the text of span with class="title" as the address
            address = a.find('span', class_='title').text
            # Get the bs4 soup of the link
            link = self.url + a['href']
            res = requests.get(link).text
            soup = BeautifulSoup(res, 'html.parser')
            # Get all a tags with the title="View Unit Details"
            for a_unit in soup.find_all('a', title='View Unit Details'):
                # Get the bs4 soup of the link
                link = self.url + a_unit['href']
                # print(link)
                res = requests.get(link).text
                soup = BeautifulSoup(res, 'html.parser')
                # Get the div with class="info"
                info = soup.find('div', class_='info')
                # Get the third h2 tag as the size
                h2s = info.find_all('h2')
                bed_bath = h2s[2].text
                price = h2s[3].text
                # Extract the price from the price text (use -1 to get upper bound)
                rent = float(price.split(
                    '$')[-1].split('-')[-1].split(' ')[0].replace(',', '').replace('*', ''))

                # we've accidentally extracted utilities pricing
                if rent < 100:
                    # use -2 to get the second-to-last price, which is actual rent
                    rent = float(price.split(
                    '$')[-2].split('-')[-1].split(' ')[0].replace(',', '').replace('*', ''))
                # Extract the bed and bath from the bed_bath text using a regex
                raw_bed = re.search(
                    r'(?:(\d+) Bedrooms)|(Efficiency)\/', bed_bath)
                raw_bath = re.search(r'\/(\d+) Baths', bed_bath)
                if raw_bath:
                    bath = float(raw_bath.group(1))
                else:
                    bath = 1
                if raw_bed.group(2) == 'Efficiency':
                    is_studio = True
                    bed = 1
                else:
                    is_studio = False
                    bed = int(raw_bed.group(1))

                available_date = '2023-08-01'
                apartments.append(Apartment(
                    address, rent, bed, bath, link, available_date, self.name, is_studio))
        return apartments