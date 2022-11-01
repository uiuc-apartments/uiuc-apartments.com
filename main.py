from datetime import datetime
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
      available_date = lookup['Available'].strip().lower()
      if available_date == 'now':
        # current date as mm/dd/yy
        available_date = datetime.now().strftime('%m/%d/%y')
    
      available = available_date != ''
    
      apartments.append(Apartment(address, rent, bed, bath, link, available, self.agency))
    
    return apartments
    
class CPM(AppFolio):
  def __init__(self):
    url = 'https://campuspm.appfolio.com/listings'
    agency = "CPM"
    super().__init__(url, agency)

class ChampaignCountyReality(AppFolio):
  def __init__(self):
    url = 'https://ccr.appfolio.com/listings'
    agency = "Champaign County Reality"
    super().__init__(url, agency)
class Weiner(AppFolio):
  def __init__(self):
    url = 'https://weinercompanies.appfolio.com/listings'
    agency = "Weiner Companies"
    super().__init__(url, agency)

class Ramshaw(AppFolio):
  def __init__(self):
    url = 'https://ram.appfolio.com/'
    agency = "Ramshaw Real Estate"
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

class Smith(BaseAgency):
  url = 'https://smith.ua.rentmanager.com/Search_Result?command=Search_Result&template=rmwbDefault&locations=1&mode=raw&propuserdef_showonweblk=Yes&orderby=aname&availabilitydate=12/31/2500&start=0&maxperpage=9999&rmwebsvc_page=1'
  agency = "Smith Apartments"
  available_when = [('8', '2023')] # tuple of month and year

  def clean_json(self, raw):
    """
    Clean the raw json string from rentmanager to make it valid json
    """
    cleaned = raw.replace('`', '"') .replace('&#10;', '').replace('\x0d', '').replace('\x0a', '')
    res = json.loads('[' + cleaned[:-1] + ']') # remove trailing comma
    return res

  def get_all(self):
    # Contains property data (rent, bed, bath, etc)
    # Note that this only has one entry per "unique" unit type.
    raw = requests.get(self.url).text
    details_json = self.clean_json(raw)
    details = {}
    for d in details_json:
      key = (int(d['ppid']), int(d['unit']))
      details[key] = d

    # We have to iterate through the json from the "rmwbAll" version of the url
    # to get all the available units for each unit type.
    res = requests.get(self.url.replace('rmwbDefault', 'rmwbAll')).text
    data = self.clean_json(res)

    apartments = []

    for unit in data:
      # Get the details for this unit type
      try:
        # use the unit it's "like" in the description to get the correct details
        u = unit['unit']
        if '-like unit ' in unit['websiteGroup']:
          u = unit['websiteGroup'].split('-like unit ')[1]
        key = (int(unit['ppid']), int(u))
        if key not in details:
          continue
      except ValueError:
        # ppid or unit was not an int, ignore this unit
        continue
      prop = details[key]

      address = prop['street1'] + prop['street2'] + unit['unit'] + ', ' + prop['city'] + ', ' + prop['state'] + ' ' + prop['zip']
      rent = float(unit['marketrent'].replace(',', '').replace('$', ''))
      bed = float(prop['bedrooms'])
      bath = float(prop['bathrooms'])
      link = 'https://smithapartments-cu.com/property-details/?pid=' + prop['ppid']

      available = False
      date_str = unit['availableDate']
      for (month, year) in self.available_when:
        # date string is formatted as "mm/dd/yyyy"
        if date_str.startswith(month + '/') and date_str.endswith('/' + year):
          available = True

      apartments.append(Apartment(address, rent, bed, bath, link, available, self.agency))
    return apartments

class Bankier(BaseAgency):
  url = 'https://www.bankierapartments.com/apartments/'
  agency = "Bankier Properties"
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
      for a in soup.find_all('a', title='View Unit Details'):
        # Get the bs4 soup of the link
        link = self.url + a['href']
        print(link)
        res = requests.get(link).text
        soup = BeautifulSoup(res, 'html.parser')
        # Get the div with class="info"
        info = soup.find('div', class_='info')
        # Get the third h2 tag as the size
        h2s = info.find_all('h2')
        bed_bath = h2s[2].text
        price = h2s[3].text
        # Extract the price from the price text (use -1 to get upper bound)
        rent = float(price.split('$')[-1].split('-')[-1].split(' ')[0].replace(',', '').replace('*',''))
        # Extract the bed and bath from the bed_bath text using a regex
        raw_bed = re.search(r'(?:(\d+) Bedrooms)|(Efficiency)\/', bed_bath)
        raw_bath = re.search(r'\/(\d+) Baths', bed_bath)
        if raw_bath:
          bath = float(raw_bath.group(1))
        else:
          bath = 1
        
        bed = 1 if raw_bed.group(2) == 'Efficiency' else int(raw_bed.group(1))
        apartments.append(Apartment(address, rent, bed, bath, link, True, self.agency))
    return apartments

class UniversityGroup(BaseAgency):
  url = 'https://ugroupcu.com/wp-admin/admin-ajax.php'
  agency = "University Group"
  fall_2023_codes = [16]
  def get_all(self):
    page = 0
    apartments = []
    while True:
      form_data = {
        'group_no': page,
        'action': 'apartment_detail',
        'available_now': self.fall_2023_codes,
        'random_order': 0,
        'roommate_check': 'N'
      }
      res = requests.post(self.url, headers={'content-type': 'application/x-www-form-urlencoded', 'user-agent': 'api-scraper'}, data=form_data).text
      if res.strip() == 'No properties listed.':
        break
      soup = BeautifulSoup(res, 'html.parser')
      # Get all links with class="more_detail"
      for a in soup.find_all('a', class_='more_detail'):
        # Get the bs4 soup of the link
        link = a['href']
        res = requests.get(link + '/', headers={'user-agent': 'api-scraper'}).text
        soup = BeautifulSoup(res, 'html.parser')
        # Get the first h2 tag under the div with class prop_detil_rgt
        address = soup.find('div', class_='prop_detil_rgt').find('h2').text
        # Get the div with id="tab-1"
        info = soup.find('div', id='tab-1')
        kinds = info.find_all('div', class_='tab-content_in_wrapp')
        for kind in kinds:
          lookup = {}
          # For each li tag with 2 divs underneath, build the lookup
          for li in kind.find('div', class_='tab-content_in_rgt').find_all('li'):
            divs = li.find_all('div')
            lookup[divs[0].text.strip()] = divs[1].text.strip()
          
          price = float(lookup['Price per month:'].replace('$', '').replace(',', ''))
          bathrooms = float(lookup.get('Bathrooms:', 0))
          availability = lookup['Availability:'].upper()
          available = availability == 'AVAILABLE AUGUST 2023'
          # bedrooms as the h4 tag with class="propert_head"
          # extract a number from the text with regex
          bedrooms_text = kind.find('h4', class_='propert_head').text.strip()
          if 'studio' in bedrooms_text.lower():
            bedrooms = 1
          else:
            bedrooms = int(re.search(r'(\d+)', bedrooms_text).group(1))
          apartments.append(Apartment(address, price, bedrooms, bathrooms, link, available, self.agency))

      page += 1
    return apartments

class Wampler(BaseAgency):
  url = 'https://wamplerapartments.com/?availability=august'
  agency = "Wampler Apartments"
  def get_all(self):
    apartments = []
    # Get all links with class="more-link"
    res = requests.get(self.url).text
    soup = BeautifulSoup(res, 'html.parser')
    for a in soup.find_all('a', class_='more-link'):
      # Get soup
      link = a['href']
      res = requests.get(link).text
      soup = BeautifulSoup(res, 'html.parser')
      # Get h3 with class="listing-address"
      address = soup.find('h3', class_='listing-address').text.strip()
      lookup = {}
      # Get all div with class="single-detail" with the key as span class="label" and value as span class="value"
      for div in soup.find_all('div', class_='single-detail'):
        spans = div.find_all('span')
        lookup[spans[0].text.strip()] = spans[1].text.strip()
      if lookup['Bedrooms:'] == 'Studio':
        bedrooms = 1
      else:
        bedrooms = int(lookup['Bedrooms:'])
      bathrooms = float(lookup['Bathrooms:'])
      available = lookup['Rent:'].upper() != 'LEASED'
      if available:
        price = float(lookup['Rent:'].replace('$', '').replace(',', ''))
      else:
        price = 0
      apartments.append(Apartment(address, price, bedrooms, bathrooms, link, available, self.agency))
    return apartments

class JSJ(BaseAgency):
  url = 'https://jsjmanagement.com/on-campus'
  agency = "JSJ Management"
  def get_all(self):
    apartments = []
    res = requests.get(self.url).text
    soup = BeautifulSoup(res, 'html.parser')
    # Get script with type="application/json" and id="search-form-config"
    script = soup.find('script', type='application/json', id='search-form-config').text
    data = json.loads(script)
    for property in data['properties']['data']:
      bedrooms = int(property['bedrooms'])
      bathrooms = float(property['bathrooms'])
      address = property['address_1']
      link = 'https://jsjmanagement.com/on-campus/listing/' + property['slug']
      price = float(property['price'].replace(',', ''))
      avail_date = property['avail_date']
      # If avail_date is later than 08-01-2023, then available
      available = datetime.strptime(avail_date, '%m-%d-%Y') > datetime.strptime('08-01-2023', '%m-%d-%Y')
      apartments.append(Apartment(address, price, bedrooms, bathrooms, link, available, self.agency))
    return apartments

class Bailey(BaseAgency):
    url = 'https://baileyapartments.com/amenities/'
    agency = "Bailey Apartments"
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
            bedrooms = int(lookup['# of Bedrooms']) if lookup['# of Bedrooms'] != 'Efficiency' else 1
            bathrooms = float(lookup['# of Baths'])
            price = float(lookup['Price (per month)'].split(' - ')[-1].replace('$', '').replace(',', ''))
            link = 'https://baileyapartments.com/apartment/' + slug
            available = lookup['Availability (AVAILABLE 2023-2024)'] == 'Available'
            apartments.append(Apartment(address, price, bedrooms, bathrooms, link, available, self.agency))
        return apartments
'''
TODO: 
ramshaw - good: https://ramshaw.com/apartments-uiuc-campus/
smith properties **in progress**
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
  Ramshaw(),
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
  GreenStreetRealty(),
  Smith(),
  Bankier(),
  UniversityGroup(),
  Wampler(),
  JSJ(),
  Bailey()
]

AllAgencies = AppFolio + AmericanCampus + Individual

def main():
  for agency in AllAgencies:
    apartments = agency.get_all()
    for apartment in apartments:
      print(apartment)


if __name__ == '__main__':
  print(Bailey().get_all())

