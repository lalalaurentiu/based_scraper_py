from scraper.Scraper import Scraper
from utils import (publish, publish_logo, create_job, show_jobs, translate_city)
from getCounty import get_county, remove_diacritics, abreviate_counties
import re

company = 'irum'
url = 'https://www.irum.ro/posturi-vacante/'

scraper = Scraper()
scraper.get_from_url(url)

jobs = []

pattern = re.compile(r"location.href='(.*)';")

abr_counties = abreviate_counties

print(abr_counties)

jobs_elements = scraper.find('div', {'id':'products'}).find_all("div", class_="card")

for job in jobs_elements:
    job_title = job.find('h5', class_='product-name').text
    job_link = re.search(pattern, job.find_all('div', class_='div-three-column')[-1].find('button').get('onclick')).group(1)    
    locations = job.find('h6', class_='h6-two-column').text.split(',')

    cities = list()
    counties = set()

    for city in locations:
        if 'VR' in city:
            city = 'VN'

        if abreviate_counties.get(city.lower().strip()):   
            county = abr_counties.get(city.lower().strip()).get('county')
            city = abreviate_counties.get(city.lower().strip()).get('city')
        else:
            city = translate_city(
                remove_diacritics(city.strip())
            )
            county = get_county(city)
        cities.append(city)
        counties.add(county)

    jobs.append(create_job(
        company=company,
        job_title=job_title,
        job_link=job_link,
        city=cities,
        county=list(counties),
        country='Romania',
    ))

for version in [1,4]:
    publish(version, company, jobs, 'APIKEY')

publish_logo(company, 'https://www.irum.ro/wp-content/uploads/2020/03/logo_IRUM.png')
show_jobs(jobs)

