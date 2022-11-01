import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import re, json

class Apartment:
    def __init__(self, address, rent, bedrooms, bathrooms, link, availability, agency):
        self.address = address
        self.rent = rent
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.link = link
        self.availability = availability
        self.agency = agency
    def __str__(self):
        return f"'{self.address}' -- ${self.rent} {self.bedrooms}BED/{self.bathrooms}BATH {'available' if self.availability else 'unavailable'} {self.link}"
    __repr__ = __str__
class BaseAgency(ABC):
  @abstractmethod
  def get_all(self):
    pass

class JSM(BaseAgency):
  url = 'https://jsmliving.com/search-available-units'
  agency = "JSM"
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
      link = self.url + article.find('a', class_='call-to-action')['href']
      # Get the first div with class="unit__card-rent"
      # Get upper price range
      rent = article.find('div', class_='unit__card-rent').text.split('RENT:')[1].split('-')[-1].replace('$','').strip()
      if rent == 'No Units Available':
        rent = 0
        available = False
      else:
        rent = int(rent)
        available = True

      # Get the text of the p tag under the div with class="unit__card-bedrooms"
      bedrooms = int(article.find('div', class_='unit__card-bedrooms').find('p').text.split(' ')[0])
      # Get the text of the p tag under the div with class="unit__card-bathrooms"
      bathrooms = float(article.find('div', class_='unit__card-bathrooms').find('p').text.split(' ')[0])
      # Get the text of the p tag under the div with class="unit__card-availability"
      # available = article.find('div', class_='unit__card-availability').text != ''
      # Add an apartment to the list
      apartments.append(Apartment(address, rent, bedrooms, bathrooms, link, available, self.agency))
    
    return apartments
  
class MHM(BaseAgency):
  url = "https://www.mhmproperties.com/apartments/?_sft_types=apartments"
  agency = "MHM"
  def get_all(self):
    apartments = []
    page = requests.get(self.url).text
    soup = BeautifulSoup(page, 'html.parser')
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
        # A regex to capture the word optional word bath followed by a number
        regex = re.compile(r'(?P<bed>\d+) Bed(?:\/(?P<bath>[\d\.]+) Bath)?.*:(?:.*\$(?P<rent>\d+,?\d+)\/(?P<kind>\w+)|.*(?P<available>LEASED!))')
        # Use regex against p tag
        match = regex.search(p.text)
        # If there is a match
        if match:
          # Get the number of bedrooms
          bedrooms = int(match.group('bed'))
          # Get the number of bathrooms
          bathrooms = float(match.group('bath') or 1)
          # Get the rent
          rent = int(match.group('rent').replace(',','') or -1)
          # Get the kind of unit
          kind = match.group('kind')
          if kind == 'person':
            rent *= bedrooms
          # Get the availability
          availability = match.group('available')
          available = availability != 'LEASED!'
          # Add an apartment to the list
          apartments.append(Apartment(address, rent, bedrooms, bathrooms, link, available, self.agency))
    
    return apartments

class Smile(BaseAgency):
  url = 'https://www.smilestudentliving.com/_dm/s/rt/actions/sites/24eaedf2/collections/appfolio-listings/ENGLISH'
  agency = "Smile"
  def get_all(self):
    apartments = []
    # request with user agent

    contents = requests.get(self.url, headers={'User-Agent': 'api-scraper'}).json()
    apartment_list = json.loads(contents['value'])
    for apartment in apartment_list:
      details = apartment['data']
      address = details['address_address1']
      available = details['available']
      bathrooms = details['bathrooms']
      bedrooms = details['bedrooms']
      # Studio
      if bedrooms == 0:
        bedrooms == 1
      market_rent = int(details['market_rent'])
      link = "https://www.smilestudentliving.com/listings/detail/" + apartment['page_item_url']
      apartments.append(Apartment(address, market_rent, bedrooms, bathrooms, link, available, self.agency))
    
    return apartments

class Roland(BaseAgency):
  url = 'http://www.roland-realty.com'
  agency = "Roland"
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
      try:
        match = bedroom_regex.search(bedrooms).group(1)
      except AttributeError:
        match = '1'
      # Get the ul with class="wsite-menu"
      ul = li.find('ul', class_='wsite-menu')
      # get the link of every a element with class='wsite-menu-subitem'
      for a in ul.find_all('a', class_='wsite-menu-subitem'):
        allLinks.append([a['href'], match])
    
    for [link, fallback_bedrooms] in allLinks:
      url = self.url + link
      page = requests.get(url).text
      soup = BeautifulSoup(page, 'html.parser')
      # Get the address as the h2 tag with class wsite-content-title as the first child of a div with id="wsite-content"
      root = soup.find('div', id='wsite-content')
      address = root.find('h2', class_='wsite-content-title').text
      status = root.find('blockquote').text.lower()
      available = 'leased' not in status
      
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
        bedroom_regex = re.compile(r'(\d+)-(?:b|B)edroom|(\d+)-BEDROOM|(One|Two|Three) Bedrooms')
        # get the number of bedrooms from the type info
        bedrooms = list(filter(lambda x: x is not None, bedroom_regex.search(typeInfo).groups()))[0]
      except AttributeError:
        bedrooms = fallback_bedrooms
      # print(bedrooms)
      price_regex = re.compile(r'\$(\d+)')
      # find all prices in price info
      prices = price_regex.findall(priceInfo)
      # turn all prices into integers and get the maximum
      rent = max([int(price) for price in prices])
      rent *= int(bedrooms)

      apartments.append(Apartment(address, rent, int(bedrooms), 0, url, available, self.agency))
       
    return apartments
  
class AppFolio(BaseAgency):
  def __init__(self, url, agency):
    self.url = url
    self.base_url = url.split('/listings')[0]
    self.agency = agency
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
      [rawBed, rawBath] = lookup['Bed / Bath'].split('/ ')
      rawBed = rawBed.split(' ')[0].strip()
      if rawBed == 'Studio':
        bed = 1
      else:
        bed = int(rawBed)
      bath = float(rawBath.split(' ')[0].strip())
      available = lookup['Available'] != ''
      apartments.append(Apartment(address, rent, bed, bath, link, available, self.agency))
    
    return apartments
    
class CPM(AppFolio):
  def __init__(self):
    url = 'https://campuspm.appfolio.com/listings?1667258359400'
    agency = "CPM"
    super().__init__(url, agency)

class ChampaignCountyReality(AppFolio):
  def __init__(self):
    url = 'https://ccr.appfolio.com/listings?1667264955192'
    agency = "Champaign County Reality"
    super().__init__(url, agency)
class Weiner(AppFolio):
  def __init__(self):
    url = 'https://weinercompanies.appfolio.com/listings?1667264295027'
    agency = "Weiner Companies"
    super().__init__(url, agency)

class AmericanCampusCommunities(BaseAgency):
  def __init__(self, url, agency, fall_term, address=None):
    self.url = url
    self.api_url = 'https://www.americancampus.com/api/nextgen/'
    self.base_url = url.split('/listings')[0]
    self.agency = agency
    self.fall_term = fall_term
    self.address = address
    super().__init__()
  def get_all(self):
    apartments = []
    print(self.api_url + self.fall_term)
    contents = requests.get(self.api_url + self.fall_term).json()
    location_lookup = {}
    for filter in contents['Filters']:
      if filter["Label"] != "Location":
        continue
        
      for value in filter["Values"]:
        location_lookup[value["ID"]] = value["Text"]
    for apartment in contents['Attributes']:
      price = apartment["MinPrice"]
      location = self.address
      for filter, list in apartment["Filters"].items():
        if filter == "Location" and location_lookup != {}:
          location = location_lookup[list[0]]
          break
      # print(apartment['Title'])
      try:
        [_, raw_bed, raw_bath] = apartment['Title'].split(' - ')
        bed_regex = re.compile(r'(\d+) Bed')
        bath_regex = re.compile(r'([\d\.]+) Bath')
        bed = int(bed_regex.search(raw_bed).group(1))
        bath = float(bath_regex.search(raw_bath).group(1))
      except ValueError:
        bed = 1
        bath = 1
      detail_url = 'https://www.americancampus.com' + apartment['DetailUrl']
      details = requests.get(detail_url).json()
      slug = details['UrlSlug']
      link = self.url + slug
      rent = price * bed
      apartments.append(Apartment(location, rent, bed, bath, link, True, self.agency))
    return apartments
class CampustownRentals(AmericanCampusCommunities):
  url = 'https://www.americancampus.com/student-apartments/il/champaign/campustown-rentals/floor-plans#/detail/'
  agency = "Campustown Rentals"
  fall_term = 'term/3a653d6c-fd95-4f30-bd85-c1188f637598'
  def __init__(self):
    super().__init__(self.url, self.agency, self.fall_term)

class Green309(AmericanCampusCommunities):
  url = 'https://www.americancampus.com/student-apartments/il/champaign/309-green/floor-plans#/detail/'
  agency = "Green 309"
  fall_term = 'term/1b950fa7-661c-4b3f-a23c-b4e111ffca30'
  address = '309 Green'
  def __init__(self):
    super().__init__(self.url, self.agency, self.fall_term, self.address)

class TowerAtThird(AmericanCampusCommunities):
  url = 'https://www.americancampus.com/student-apartments/il/champaign/tower-at-3rd/floor-plans#/detail/'
  agency = "Tower at Third"
  fall_term = 'term/d8b37712-193a-42f5-b416-b4f6a23d6a3e'
  address = 'Tower at Third'
  def __init__(self):
    super().__init__(self.url, self.agency, self.fall_term, self.address)

class Lofts54(AmericanCampusCommunities):
  url = 'https://www.americancampus.com/student-apartments/il/champaign/lofts54/floor-plans#/detail/'
  agency = "Lofts 54"
  fall_term = 'term/280fcf82-6d95-42b9-9ed3-ec9f6decd476'
  address = 'Lofts 54 address'
  def __init__(self):
    super().__init__(self.url, self.agency, self.fall_term, self.address)
class SuitesAtThird(AmericanCampusCommunities):
  url = 'https://www.americancampus.com/student-apartments/il/champaign/the-suites-at-3rd/floor-plans#/detail/'
  agency = "Suites at Third"
  fall_term = 'term/0d3da1dc-3c4a-44e9-996e-bf8b9001bf5f'
  address = 'Suites at Third address'
  def __init__(self):
    super().__init__(self.url, self.agency, self.fall_term, self.address)

class GreenStreetRealty(BaseAgency):
  url = 'https://www.greenstrealty.com/modules/extended/propertySearch'
  agency = "Green Street Realty"
  terms = ['Available August 2023']
  def get_all(self):
    res = requests.post(self.url, headers={'content-type': 'application/x-www-form-urlencoded'}, data={'query': '/'.join(self.terms), 'show_map': False}).text
    soup = BeautifulSoup(res, 'html.parser') 
    apartments = []
    # get all divs with class property-item-data
    for div in soup.find_all('div', class_='property-item-data'):
      # get all divs with class property-item-data
      try:
        address = div.find('div', class_='property-item-title').text.replace('\n',', ').replace('\t','').strip()[2:]
        link = 'https://www.greenstrealty.com' + div.find('a', class_='cms-btn cms-btn-primary')['href']
        # print(address)
        kinds = div.find_all('div', class_='property-item-info')
        for kind in kinds:
          # print(kind.text)
          try:
            raw_bed_txt = kind.find('div', class_='beds').text.lower()
            if 'studio' in raw_bed_txt:
              bed = 1
            else:
              bed = int(raw_bed_txt.split(' ')[0])
          except ValueError:
            bed = 0
          bath = float(kind.find('div', class_='baths').text.split(' ')[0])

          raw_price = kind.find('div', class_='price').text
          multiplier = 1
          if '/Bed' in raw_price:
            raw_price = raw_price.split('/')[0]
            multiplier = bed
          price = int(raw_price.replace('$', '').replace(',', ''))
          rent = price * multiplier

          apartments.append(Apartment(address, rent, bed, bath, link, True, self.agency))
      except ValueError:
        continue
    return apartments

'''
TODO: 
ramshaw - good: https://ramshaw.com/apartments-uiuc-campus/
smith properties - good: https://smithapartments-cu.com/
bankier - good: https://www.bankierapartments.com/apartments
university group - mid: https://ugroupcu.com/apartment-search/
wampler - mid: https://wamplerapartments.com/
JSJ - mid : https://jsjmanagement.com/on-campus/query/bedrooms/any/bathrooms/any/types/any/price/any
Illini Tower - hard to scrape: https://www.illinitoweruiuc.com/floor-plans/2-bedroom/
Latitude - pricy: https://www.livelatitude.com/champaign/latitude/student/
here/707/octave - no public pricing
Bailey - small https://baileyapartments.com/apartment/
'''
AppFolio = [
  CPM(),
  Weiner(),
  ChampaignCountyReality(),
]

AmericanCampus = [
  CampustownRentals(),
  Green309(),
  TowerAtThird(),
  Lofts54(),
  SuitesAtThird(),
]
Individual = [
  JSM(),
  MHM(),
  Smile(),
  Roland(),
  GreenStreetRealty()
]

AllAgencies = AppFolio + AmericanCampus + Individual

for agency in AllAgencies:
  apartments = agency.get_all()
  for apartment in apartments:
    print(apartment)