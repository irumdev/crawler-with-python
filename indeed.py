import requests
from bs4 import BeautifulSoup


def extract_indeed_pages(url):
    result = requests.get(url)
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
    for n in range(last_page):
        print(f"&start={n*50}")