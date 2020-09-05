from indeed import *

INDEED_URL = "https://kr.indeed.com/jobs?q=php&limit=50"

last_indeed_page = extract_indeed_pages(INDEED_URL)
extract_indeed_jobs(last_indeed_page)