import requests
from bs4 import BeautifulSoup
from uiuc_apartments.shared import AgencyBase, Apartment
import re

class UniversityGroup(AgencyBase):
    url = 'https://ugroupcu.com/building-list/'
    name = "University Group"
    fall_2023_codes = [16]

    def get_all(self):
        # page = 0
        apartments = []
            # form_data = {
            #     'group_no': page,
            #     'action': 'apartment_detail',
            #     'available_now': self.fall_2023_codes,
            #     'random_order': 0,
            #     'roommate_check': 'N'
            # }
        res = requests.post(self.url, headers={
                            'user-agent': 'api-scraper'}).text
        if res.strip() == 'No properties listed.' or '500 Error' in res:
            return []
        soup = BeautifulSoup(res, 'html.parser')

        # Get all links with class="more_detail"
        for a in soup.find_all('a', class_='more_detail'):
            # Page has a "sort" button that does not lead anywhere
            if not a.has_attr('href'):
                continue    
            # Get the bs4 soup of the link
            link = a['href']
            res = requests.get(
                link, headers={'user-agent': 'api-scraper'}).text
            # print(res)
            soup = BeautifulSoup(res, 'html.parser')
            # Get the first h2 tag under the div with class prop_detil_rgt
            # print('====', link)
            # print(res)
            address = soup.find(
                'div', class_='prop_detil_rgt').find('h2').text
            # Get the div with id="tab-1"
            info = soup.find('div', id='tab-1')
            kinds = info.find_all('div', class_='tab-content_in_wrapp')
            for kind in kinds:
                lookup = {}
                # For each li tag with 2 divs underneath, build the lookup
                for li in kind.find('div', class_='tab-content_in_rgt').find_all('li'):
                    divs = li.find_all('div')
                    lookup[divs[0].text.strip()] = divs[1].text.strip()

                price = float(lookup['Price per month:'].replace(
                    '$', '').replace(',', ''))
                bathrooms = float(lookup.get('Bathrooms:', 0))
                availability = lookup['Availability:'].lower()
                if 'not available' in availability:
                    continue
                available_date = '2023-08-01' if 'available august 2023' in availability else None
                # bedrooms as the h4 tag with class="propert_head"
                # extract a number from the text with regex
                bedrooms_text = kind.find(
                    'h4', class_='propert_head').text.strip()
                if 'studio' in bedrooms_text.lower():
                    is_studio = True
                    bedrooms = 1
                else:
                    is_studio = False
                    try:
                        bedrooms = int(
                            re.search(r'(\d+)', bedrooms_text).group(1))
                    except AttributeError:
                        bedrooms = 0
                apartments.append(Apartment(
                    address, price, bedrooms, bathrooms, link, available_date, self.name, is_studio))

            # page += 1
        # print("returning here")
        return apartments