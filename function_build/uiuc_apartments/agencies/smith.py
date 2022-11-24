import requests
from uiuc_apartments.shared import AgencyBase, Apartment
import json

class Smith(AgencyBase):
    url = 'https://smith.ua.rentmanager.com/Search_Result?command=Search_Result&template=rmwbDefault&locations=1&mode=raw&propuserdef_showonweblk=Yes&orderby=aname&availabilitydate=12/31/2500&start=0&maxperpage=9999&rmwebsvc_page=1'
    name = "Smith Apartments"

    def clean_json(self, raw):
        """
        Clean the raw json string from rentmanager to make it valid json
        """
        cleaned = raw.replace('`', '"') .replace(
            '&#10;', '').replace('\x0d', '').replace('\x0a', '')
        res = json.loads('[' + cleaned[:-1] + ']')  # remove trailing comma
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

            address = prop['street1'] + prop['street2'] + unit['unit'] + \
                ', ' + prop['city'] + ', ' + prop['state'] + ' ' + prop['zip']
            rent = float(unit['marketrent'].replace(',', '').replace('$', ''))
            bed = int(prop['bedrooms'])
            bath = float(prop['bathrooms'])
            is_studio = False
            link = 'https://smithapartments-cu.com/property-details/?pid=' + \
                prop['ppid']

            date_str = unit['availableDate']

            apartments.append(Apartment(address, rent, bed,
                                        bath, link, date_str, self.name, is_studio))
        return apartments
