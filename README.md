# uiuc-apartments-api

## Improving the Apartment Search Process at UIUC

### Problem

**finding apartments in champaign sucks!**
+ the only way is to go to each agency site, and check if they have something that meets your criteria
+ apartments.com / aggregators suck because each company has to upload their own apartments to each aggregator site, which they don't do

### Introducting \<cool name here>

+ We will build an aggregator site that goes to each agency and downloads the properties using a webscaper + internal APIs
+ users can just visit our site to find properties they want, which will actually be up-to-date with all properties

### How it works

1. We scrape each champaign agency site for properties, once per hour to get most updated list + statuses
2. A user visits our site, and can use simple filters to narrow down agency, location, bedrooms, bathrooms, price
3. The user can now view the properties that meet their criteria

### Implementation

1. Finish scraper
2. Have scraper turn data into database of some sort - mongo/postgres/i dont care
3. Write backend server code to interface with the database
4. Write simple frontend
5. Deploy frontend/backend to cloud (GCP/i dont care)
6. Improve frontend, get public URL
7. post on reddit and PROFIT!!!
