import requests
from bs4 import BeautifulSoup
from uiuc_apartments.shared import AgencyBase, Apartment

class GreenStreetRealty(AgencyBase):
    url = 'https://www.greenstrealty.com/modules/extended/propertySearch'
    name = "Green Street Realty"
    terms = ['Available August 2023']

    def get_all(self):
        res = requests.post(self.url, headers={'content-type': 'application/x-www-form-urlencoded'}, data={
                            'query': '/'.join(self.terms), 'show_map': False}).text
        soup = BeautifulSoup(res, 'html.parser')
        apartments = []
        # get all divs with class property-item-data
        for div in soup.find_all('div', class_='property-item-data'):
            # get all divs with class property-item-data
            try:
                address = div.find(
                    'div', class_='property-item-title').text.replace('\n', ', ').replace('\t', '').strip()[2:]
                link = 'https://www.greenstrealty.com' + \
                    div.find('a', class_='cms-btn cms-btn-primary')['href']
                # print(address)
                kinds = div.find_all('div', class_='property-item-info')
                for kind in kinds:
                    # print(kind.text)
                    is_studio = False
                    try:
                        raw_bed_txt = kind.find(
                            'div', class_='beds').text.lower()
                        raw_bed_txt = raw_bed_txt.replace('+', '')
                        if 'studio' in raw_bed_txt:
                            is_studio = True
                            bed = 1
                        else:
                            bed = int(raw_bed_txt.split(' ')[0])
                    except ValueError:
                        bed = 0
                    bath = float(
                        kind.find('div', class_='baths').text.split(' ')[0])

                    raw_price = kind.find('div', class_='price').text
                    multiplier = 1
                    if '/Bed' in raw_price:
                        raw_price = raw_price.split('/')[0]
                        multiplier = bed
                    price = int(raw_price.replace('$', '').replace(',', ''))
                    rent = price * multiplier

                    available_date = '2023-08-01'

                    apartments.append(Apartment(
                        address, rent, bed, bath, link, available_date, self.name, is_studio))
            except ValueError:
                continue
        return apartments