import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=php&jt=fulltime&limit=50{LIMIT}"


def extract_indeed_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", "pagination")
    links = pagination.find_all("a")

    pages = []
    for link in links[:-1]:
        # pages.append(link.find("span").string)
        pages.append(int(link.string))  # 태그가 여러개 중첩되어도 string메소드는 최종 text만 가져옴

    max_page = pages[-1]
    return max_page


def extract_indeed_jobs(last_page):
    jobs = []

    for page_num in range(last_page):
        print(f"Crawling page {page_num}")
        result = requests.get(f"{URL}&start={page_num*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", "jobsearch-SerpJobCard")

        for rst in results:
            title = rst.find("a", "jobtitle")["title"]
            company = rst.find("div", "sjcl").find("span", "company")
            location = rst.find("div", "recJobLoc")["data-rc-loc"]
            job_id = rst["data-jk"]
            if company is None or company.string is None:
                continue
            company = company.string.strip()
            job = {
                "title": title,
                "company": company,
                "location": location,
                "job_id": f"https://kr.indeed.com/viewjob?jk={job_id}",
            }
            jobs.append(job)
    return jobs


def get_indeed_jobs():
    last_indeed_page = extract_indeed_pages()
    indeed_jobs = extract_indeed_jobs(last_indeed_page)
    return indeed_jobs