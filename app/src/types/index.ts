export interface Apartment {
  address: string
  agency: string
  available_date: string
  bathrooms: number
  bedrooms: number
  id: number
  is_studio: boolean
  link: string
  rent: number
  latitude: number
  longitude: number
}

export type Filter = {
  minBedrooms: number
  maxBedrooms: number
  minBathrooms: number
  maxBathrooms: number
  dateRange: Array<Date>
  minRent: number
  maxRent: number
  selectedAgencies: Array<string>
}
