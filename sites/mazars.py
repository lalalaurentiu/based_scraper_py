from scraper_peviitor import Scraper, Rules, loadingData
import uuid
import json

url = " https://www.mazarscareers.com/ro/wp-admin/admin-ajax.php?action=get_job_listing_html&searchTerm=&form=contract%3D%26location%3D%26service%3D&amount=-1&location="

company = {"company": "Mazars"}
finalJobs = list()

scraper = Scraper()
rules = Rules(scraper)

scraper.url = url

html = scraper.getJson()
scraper.soup = html.get("html")

jobs = rules.getTags("article", {"class": "JobResult"})

for job in jobs:
    id = uuid.uuid4()
    job_title = job.find("p", {"class":"job-title"}).text.strip()
    job_link = job.find("a").get("href")
    country = "Romania"
    city = job.find_all("p")[1].text.split(":")[1].strip()

    print(job_title + " -> " + city)
    
    finalJobs.append({
        "id": str(id),
        "job_title": job_title,
        "job_link": job_link,
        "country": country,
        "city": city,
        "company": company.get("company")
    })

print("Total jobs: " + str(len(finalJobs)))

loadingData(finalJobs, "182b157-bb68-e3c5-5146-5f27dcd7a4c8", company.get("company"))

logoUrl = "https://www.mazarscareers.com/ro/wp-content/themes/mazars-2020/assets/images/mazars-logo.png"

scraper.session.headers.update({
    "Content-Type": "application/json",
})
scraper.post( "https://api.peviitor.ro/v1/logo/add/" ,json.dumps([
    {
        "id":company.get("company"),
        "logo":logoUrl
    }
]))