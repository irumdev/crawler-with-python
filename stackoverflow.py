import requests
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com/jobs?q=python"


def extract_stackoverflow_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", "s-pagination")
    links = pagination.find_all("a", "s-pagination--item")

    pages = []
    for link in links:
        page = link.find("span").string
        if page.isdigit():
            pages.append(int(page))

    max_page = pages[-1]
    return max_page


def extract_stackoverflow_jobs(last_page):
    jobs = []

    for page_num in range(1, last_page):
        print(f"Crawling StackOverFlow page {page_num}")
        result = requests.get(f"{URL}&pg={page_num}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", "js-result")

        for rst in results:
            section = rst.find("div", "fl1")
            title = section.find("h2", "mb4").find("a")["title"]
            company = section.find("h3", "mb4").find("span")
            location = (
                section.find("h3", "mb4").find("span", "fc-black-500").string.strip()
            )
            if company is None or company.string is None:
                continue
            company = company.string.strip()
            job_id = rst["data-jobid"]
            job = {
                "title": title,
                "company": company,
                "location": location,
                "job_id": f"https://stackoverflow.com/jobs/{job_id}",
            }
            jobs.append(job)
    return jobs


def get_stackoverflow_jobs():
    last_stackoverflow_page = extract_stackoverflow_pages()
    stackoverflow_jobs = extract_stackoverflow_jobs(last_stackoverflow_page)
    return stackoverflow_jobs