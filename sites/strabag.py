from scraper.Scraper import Scraper
from utils import publish_or_update, publish_logo, create_job, show_jobs, translate_city
from getCounty import GetCounty

_counties = GetCounty()
def remove_words(text, words):
    for word in words:
        text = text.replace(word, "")
    return text


url = "https://jobboerse.strabag.at/inc/jobsuche_2025_v1.php"

company = "Strabag"
jobs = list()

data = {
    "MIME Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "morejobs": 1,
    "search": "Romania",
    "radius": 50,
    "language": "RO",
    "status": 1,
}

while True:

    scraper = Scraper()
    response = scraper.post(url, data=data).text
    scraper.__init__(response, "html.parser")

    jobs_containers = scraper.find_all("div", class_="search-entry__container")

    if len(jobs_containers) == 0:
        break

    for job_container in jobs_containers:

        jobs.append(
            create_job(
                job_title=job_container.find(
                    "h4", class_="search-entry__headline")
                .text.strip(),
                job_link=job_container.find("a")["href"],
                country="Romania",
                company=company,
            )
        )

    data["morejobs"] += 1

publish_or_update(jobs)

publish_logo(company, "https://jobboerse.strabag.at/img/strabag-logo-300px.png")
show_jobs(jobs)
