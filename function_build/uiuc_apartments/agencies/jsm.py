import requests
from bs4 import BeautifulSoup
from uiuc_apartments.shared import AgencyBase, Apartment


class JSM(AgencyBase):
    url = 'https://jsmliving.com/search-available-units'
    name = "JSM"

    def get_all(self):
        apartments = []
        page = requests.get(self.url).text
        soup = BeautifulSoup(page, 'html.parser')
        # Get all article elements with the role="article" attribute
        articles = soup.find_all('article', role='article')
        # Loop through each article and get the data we want
        for article in articles:
            # Get the address as the a link with the hreflang="en" attribute
            address = article.find('a', hreflang='en').text.strip()
            # Get the link as the a link with the class="call-to-action" attribute
            link = self.url + \
                article.find('a', class_='call-to-action')['href']
            # Get the first div with class="unit__card-rent"
            # Get upper price range
            rent = article.find('div', class_='unit__card-rent').text.split(
                'RENT:')[1].split('-')[-1].replace('$', '').strip()
            if rent == 'No Units Available':
                continue
            else:
                rent = int(rent)
                available_date = '2021-01-01'

            # Get the text of the p tag under the div with class="unit__card-bedrooms"
            bedrooms = int(article.find(
                'div', class_='unit__card-bedrooms').find('p').text.split(' ')[0])
            is_studio = False
            if bedrooms == 0:
                is_studio = True
                bedrooms = 1
            # Get the text of the p tag under the div with class="unit__card-bathrooms"
            bathrooms = float(article.find(
                'div', class_='unit__card-bathrooms').find('p').text.split(' ')[0])
            # Get the text of the p tag under the div with class="unit__card-availability"
            # available = article.find('div', class_='unit__card-availability').text != ''
            # Add an apartment to the list
            apartments.append(Apartment(
                address, rent, bedrooms, bathrooms, link, available_date, self.name, is_studio))

        return apartments
