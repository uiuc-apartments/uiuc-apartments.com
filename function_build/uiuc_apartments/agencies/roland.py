import requests
from bs4 import BeautifulSoup
from uiuc_apartments.shared import AgencyBase, Apartment
import re

class Roland(AgencyBase):
    url = 'http://www.roland-realty.com'
    name = "Roland"

    def get_all(self):
        apartments = []
        page = requests.get(self.url).text
        soup = BeautifulSoup(page, 'html.parser')
        # Get the parent of the link with href=/on-campus-apartments.html
        parent = soup.find('a', href='/on-campus-apartments.html').parent
        # Get the ul with class="wsite-menu"
        ul = parent.find('ul', class_='wsite-menu')
        # Get all the direct li children of the ul
        lis = ul.findChildren('li', recursive=False)
        # Loop through each li
        allLinks = []
        for li in lis:
            bedrooms = li.find('span', class_='wsite-menu-title').text
            bedroom_regex = re.compile(r'(\d+)\+? Bedroom')
            is_studio = False
            try:
                match = bedroom_regex.search(bedrooms).group(1)
            except AttributeError:
                match = '1'
                is_studio = True
            # Get the ul with class="wsite-menu"
            ul = li.find('ul', class_='wsite-menu')
            # get the link of every a element with class='wsite-menu-subitem'
            for a in ul.find_all('a', class_='wsite-menu-subitem'):
                allLinks.append([a['href'], match, is_studio])

        for [link, fallback_bedrooms, is_studio] in allLinks:
            url = self.url + link
            page = requests.get(url).text
            soup = BeautifulSoup(page, 'html.parser')
            # Get the address as the h2 tag with class wsite-content-title as the first child of a div with id="wsite-content"
            root = soup.find('div', id='wsite-content')
            address = root.find('h2', class_='wsite-content-title').text
            status = root.find('blockquote').text.lower()
            available_date = None
            if 'leased' not in status:
                available_date = '2023-08-01'
            # Find next div of blockquote with no class and a child div with class="wsite-multicol"
            table = None
            start = root.find('blockquote')
            while table is None:
                table = start.find_next_sibling('div', class_=None)
                if table:
                    table = table.find('table', class_='wsite-multicol-table')
                start = start.parent
            # print(table.text)
            tr = table.find('tr')
            tds = tr.findChildren('td', recursive=False)
            typeInfo = tds[1].text
            i = 1
            while 'price' not in tds[i].text.lower():
                i += 1
            priceInfo = tds[i].text.lower()
            # print(typeInfo)

            try:
                bedroom_regex = re.compile(
                    r'(\d+)-(?:b|B)edroom|(\d+)-BEDROOM|(One|Two|Three) Bedrooms')
                # get the number of bedrooms from the type info
                bedrooms = list(filter(lambda x: x is not None,
                                       bedroom_regex.search(typeInfo).groups()))[0]
            except AttributeError:
                bedrooms = fallback_bedrooms
            # print(bedrooms)
            price_regex = re.compile(r'\$(\d+)')
            # find all prices in price info
            prices = price_regex.findall(priceInfo)
            # turn all prices into integers and get the maximum
            rent = max([int(price) for price in prices])
            rent *= int(bedrooms)

            apartments.append(Apartment(address, rent, int(
                bedrooms), 0, url, available_date, self.name, is_studio))

        return apartments