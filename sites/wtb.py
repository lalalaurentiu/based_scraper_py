from scraper.Scraper import Scraper
from utils import create_job, show_jobs, publish_or_update, publish_logo

url = "https://www.wtb.ro/category/careers/category/careers/"

company = "WTB"
finalJobs = list()

scraper = Scraper()
scraper.get_from_url(url)
page = 1

jobs = scraper.find_all(
    "h3", {"class": "t-entry-title h5"}
)

while jobs:
    for job in jobs:
        job_title = job.text.replace("JOB:", "").strip()
        job_link = job.find("a").get("href")

        finalJobs.append(
            create_job(
                job_title=job_title,
                job_link=job_link,
                company=company,
                country="Romania",
                city="Bucuresti",
                county="Bucuresti",
            )
        )

    page += 1
    scraper.get_from_url(url + f"category/careers/category/careers/?%&upage={page}")
    jobs = scraper.find_all( "h3", {"class": "t-entry-title h5"})

publish_or_update(finalJobs)
publish_logo(company, "https://www.wtb.ro/wp-content/uploads/2018/04/logoblack.svg")
show_jobs(finalJobs)
