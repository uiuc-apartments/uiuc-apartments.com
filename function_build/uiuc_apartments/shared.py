from abc import ABC, abstractmethod


class Apartment:
    def __init__(self, address, rent, bedrooms, bathrooms, link, available_date, agency, is_studio):
        self.address = address
        self.rent = rent
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.link = link
        self.available_date = available_date
        self.agency = agency
        self.is_studio = is_studio

    def __str__(self):
        info = 'Studio' if self.is_studio else f'{self.bedrooms} beds/{self.bathrooms} baths'
        return f"<Apartment ${self.rent}/month {info} {self.available_date} {self.agency}>"
    __repr__ = __str__


class AgencyBase(ABC):
    name: str
    url: str

    @abstractmethod
    def get_all(self):
        pass
