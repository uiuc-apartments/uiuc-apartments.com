import requests
from uiuc_apartments.shared import AgencyBase, Apartment
import re

class AmericanCampusBase(AgencyBase):
    def __init__(self, url, agency, fall_term, address=None):
        self.url = url
        self.api_url = 'https://www.americancampus.com/api/nextgen/'
        self.base_url = url.split('/listings')[0]
        self.name = agency
        self.fall_term = fall_term
        self.address = address
        super().__init__()

    def get_all(self):
        apartments = []
        # print(self.api_url + self.fall_term)
        contents = requests.get(self.api_url + self.fall_term).json()
        location_lookup = {}
        for search_filter in contents['Filters']:
            if search_filter["Label"] != "Location":
                continue

            for value in search_filter["Values"]:
                location_lookup[value["ID"]] = value["Text"]
        for apartment in contents['Attributes']:
            price = apartment["MinPrice"]
            location = self.address
            for search_filter, values in apartment["Filters"].items():
                if search_filter == "Location" and location_lookup != {}:
                    location = location_lookup[values[0]]
                    break
            # print(apartment['Title'])
            is_studio = False
            try:
                [_, raw_bed, raw_bath] = apartment['Title'].split(' - ')
                bed_regex = re.compile(r'(\d+) Bed')
                bed = int(bed_regex.search(raw_bed).group(1))
                bath_regex = re.compile(r'([\d\.]+) Bath')
                bath = float(bath_regex.search(raw_bath).group(1))
            except ValueError:
                is_studio = True
                bed = 1
                bath = 1

            detail_url = 'https://www.americancampus.com' + \
                apartment['DetailUrl']
            details = requests.get(detail_url).json()
            slug = details['UrlSlug']
            link = self.url + slug
            rent = price * bed
            available_date = '2023-08-01'
            apartments.append(Apartment(
                location, rent, bed, bath, link, available_date, self.name, is_studio))
        return apartments


class CampustownRentals(AmericanCampusBase):
    url = 'https://www.americancampus.com/student-apartments/il/champaign/campustown-rentals/floor-plans#/detail/'
    name = "Campustown Rentals"
    fall_term = 'term/3a653d6c-fd95-4f30-bd85-c1188f637598'

    def __init__(self):
        super().__init__(self.url, self.name, self.fall_term)


class Green309(AmericanCampusBase):
    url = 'https://www.americancampus.com/student-apartments/il/champaign/309-green/floor-plans#/detail/'
    name = "Green 309"
    fall_term = 'term/1b950fa7-661c-4b3f-a23c-b4e111ffca30'
    address = '309 Green St'

    def __init__(self):
        super().__init__(self.url, self.name, self.fall_term, self.address)


class TowerAtThird(AmericanCampusBase):
    url = 'https://www.americancampus.com/student-apartments/il/champaign/tower-at-3rd/floor-plans#/detail/'
    name = "Tower at Third"
    fall_term = 'term/d8b37712-193a-42f5-b416-b4f6a23d6a3e'
    address = ' 302 E John St'

    def __init__(self):
        super().__init__(self.url, self.name, self.fall_term, self.address)


class Lofts54(AmericanCampusBase):
    url = 'https://www.americancampus.com/student-apartments/il/champaign/lofts54/floor-plans#/detail/'
    name = "Lofts 54"
    fall_term = 'term/280fcf82-6d95-42b9-9ed3-ec9f6decd476'
    address = '309 E Green St'

    def __init__(self):
        super().__init__(self.url, self.name, self.fall_term, self.address)


class SuitesAtThird(AmericanCampusBase):
    url = 'https://www.americancampus.com/student-apartments/il/champaign/the-suites-at-3rd/floor-plans#/detail/'
    name = "Suites at Third"
    fall_term = 'term/0d3da1dc-3c4a-44e9-996e-bf8b9001bf5f'
    address = '707 S 3rd St'

    def __init__(self):
        super().__init__(self.url, self.name, self.fall_term, self.address)

AmericanCampus = [
  CampustownRentals(),
  Green309(),
  TowerAtThird(),
  Lofts54(),
  SuitesAtThird(),
]