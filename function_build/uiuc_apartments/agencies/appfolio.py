from uiuc_apartments.shared import AgencyBase, Apartment
from bs4 import BeautifulSoup
import requests
from datetime import datetime


class AppFolioBase(AgencyBase):
    def __init__(self, url, agency):
        self.url = url
        self.base_url = url.split('/listings')[0]
        self.name = agency
        super().__init__()

    def get_all(self):
        apartments = []
        contents = requests.get(self.url).text
        soup = BeautifulSoup(contents, 'html.parser')
        # get all divs with class listing-item__body
        divs = soup.find_all('div', class_='listing-item__body')
        for div in divs:
            lookup = {}
            # get all divs with class detail-box__item
            for detail in div.find_all('div', class_='detail-box__item'):
                # find dt element
                key = detail.find('dt').text
                value = detail.find('dd').text
                lookup[key] = value
            # get span with js-listing-address
            address = div.find('span', class_='js-listing-address').text
            # get link href with class js-link-to-detail
            link = self.base_url + div.find('a', target="_blank")['href']

            rent = int(lookup['RENT'].replace('$', '').replace(',', ''))
            # some listings do not have bed / bath provided
            [rawBed, rawBath] = lookup.get('Bed / Bath', '0 / 0').split('/ ')
            rawBed = rawBed.split(' ')[0].strip()
            if rawBed == 'Studio':
                is_studio = True
                bed = 1
            else:
                is_studio = False
                bed = int(rawBed)
            bath = float(rawBath.split(' ')[0].strip())
            available_date = lookup.get('Available', None)
            if available_date:
                available_date = available_date.strip().lower()
            if available_date == 'now':
                # current date as mm/dd/yy
                available_date = datetime.now().strftime('%m/%d/%y')

            apartments.append(Apartment(address, rent, bed, bath,
                                        link, available_date, self.name, is_studio))

        return apartments


class CPM(AppFolioBase):
    def __init__(self):
        url = 'https://campuspm.appfolio.com/listings'
        name = "CPM"
        super().__init__(url, name)


class ChampaignCountyReality(AppFolioBase):
    def __init__(self):
        url = 'https://ccr.appfolio.com/listings'
        name = "Champaign County Reality"
        super().__init__(url, name)


class Weiner(AppFolioBase):
    def __init__(self):
        url = 'https://weinercompanies.appfolio.com/listings'
        name = "Weiner Companies"
        super().__init__(url, name)


class Ramshaw(AppFolioBase):
    def __init__(self):
        url = 'https://ram.appfolio.com/'
        name = "Ramshaw Real Estate"
        super().__init__(url, name)

AppFolio = [
  CPM(),
  Weiner(),
  ChampaignCountyReality(),
  Ramshaw(),
]