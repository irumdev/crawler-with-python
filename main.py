from indeed import *
from stackoverflow import *
from save import *


indeed_jobs = get_indeed_jobs()
stackoverflow_jobs = get_stackoverflow_jobs()
jobs = indeed_jobs + stackoverflow_jobs
save_to_file(jobs)