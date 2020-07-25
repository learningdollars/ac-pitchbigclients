from selenium import webdriver
from bs4 import BeautifulSoup
from time import strftime
import datetime
import time
import csv
import os

from ld_skills import get_all_skills
from ld_skills import modify
from ld_skill_link import get_link

def indeed_setup():
  PATH = "./chromedriver" 
  options = webdriver.ChromeOptions()
  options.add_argument("--start-maximized")

  URL = "https://www.indeed.com/jobs?q=software+developer&l=Remote&rbl=Remote&jlid=aaa2b906602aa8f5&jt=contract"
  driver = webdriver.Chrome(PATH, chrome_options=options)
  # driver = webdriver.Chrome(chrome_options=options) # gobi version
  driver.get(URL)

  job_links = []
  while True:
    try:
      get_jobs(job_links, driver)
    except:
      try:
        driver.find_element_by_class_name('popover-x-button-close').click()
        get_jobs(job_links, driver)
      except:
        break

  scraper(job_links, driver)
  driver.close()

def get_jobs(job_links, driver):
  all_jobs = driver.find_elements_by_class_name('result')
  for job in all_jobs:
    link = job.find_element_by_tag_name('h2').find_element_by_tag_name('a').get_attribute('href')
    job_links.append(link)
  pagination = driver.find_element_by_class_name('pagination').find_elements_by_tag_name('li')
  last_li = pagination[-1]
  last_li.find_element_by_tag_name('a').click()

def scraper(job_links, driver):

  # Get all LD skills to compare and extract skills from the job description
  ld_skills = get_all_skills(driver)
  
  today = datetime.datetime.now()
  filename = 'indeed_jobs_' + str(today.day) + '_' + strftime("%b") + '_' + str(today.year) + '_' + str(today.hour) + '_' + str(today.minute) + '.csv'

  with open(os.path.dirname(os.path.abspath('indeed_jobs')) + '/indeed_jobs/' + filename, 'w', encoding='UTF-16', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['posted_date', 'skills', 'job_name', 'job_type', 'company_name', 'description', 'ld_link'])

    for link in job_links:
      driver.get(link)
      detail = driver.find_element_by_class_name('jobsearch-JobComponent')
      result = detail.get_attribute('innerHTML')
      soup   = BeautifulSoup(result, 'html.parser')

      # Extracting the required data
      job_name     = soup.find("h3").text
      company_name = soup.find("div", class_ = 'icl-u-lg-mr--sm').text
      job_type     = soup.find("span", class_ = 'jobsearch-JobMetadataHeader-item').text
      description  = soup.find("div", class_ = 'jobsearch-jobDescriptionText').text
      date         = soup.find("div", class_ = 'jobsearch-JobMetadataFooter').text.split()

      # Change date into N days ago format
      index       = date.index('-')+1
      parsed_date = date[index:]
      final_date  = parsed_date[0:parsed_date.index('-')]
      posted_date = ' '.join(final_date)

      # Change N days ago format into date format
      if '30+' in posted_date:
        pass
      else:
        if (posted_date == 'Today'):
          posted_date = datetime.date.today()
        elif (posted_date == 'Just posted'):
          posted_date = datetime.date.today()
        else:
          if (posted_date == '1 day ago'):
            dt = datetime.timedelta(days = 1)
          else:
            parsed_date   = [posted_date.split()[:2]]
            if (parsed_date[0][1] == 'hour'):
              parsed_date[0][1] = 'hours'
            time_dict = dict((index,float(value)) for value,index in parsed_date)
            dt = datetime.timedelta(**time_dict)
          posted_date = datetime.datetime.now() - dt
          posted_date = posted_date.date()

      # To extract skills from description
      desc_list = description.lower().split()
      modified_desc_list = []
      skills = []
      for item in desc_list:
        modified_desc_list.append(modify(item))
      for skill in ld_skills:
        if skill in modified_desc_list:
          skills.append(skill)

      ld_link = get_link(skills, driver)
      writer.writerow([posted_date, skills, job_name, job_type, company_name, description, ld_link])
      print('New job record added: ', job_name)

    print('\nSuccessfully created a new csv file for indeed.com jobs - ' + filename + '.')  
