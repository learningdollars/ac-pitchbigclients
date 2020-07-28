from selenium import webdriver
from bs4 import BeautifulSoup
from dateutil.parser import parse
from time import strftime
import datetime
import csv
import os

from ld_skills import get_all_skills
from ld_skills import modify
from ld_skill_link import get_link

def weworkremotely_setup():
  PATH = "./chromedriver" 
  options = webdriver.ChromeOptions()
  options.add_argument("--start-maximized")

  URL = "https://weworkremotely.com/categories/remote-programming-jobs"
  # driver = webdriver.Chrome(PATH, chrome_options=options) # anisha version
  driver = webdriver.Chrome(chrome_options=options) # gobi version
  driver.get(URL)

  job_container = driver.find_element_by_class_name('jobs-container')
  all_jobs = job_container.find_elements_by_class_name('feature')
  job_links = []

  # Sraping all job links
  for job in all_jobs:
    try:
      link = job.find_elements_by_tag_name('a')[1].get_attribute('href')
    except:
      link = job.find_elements_by_tag_name('a')[0].get_attribute('href')
    job_links.append(link)
  
  scraper(job_links, driver)

def scraper(job_links, driver):
  # Get all LD skills to compare and extract skills from the job description
  ld_skills = get_all_skills(driver)

  today = datetime.datetime.now()
  filename = 'weworkremotely_jobs_' + str(today.day) + '_' + strftime("%b") + '_' + str(today.year) + '_' + str(today.hour) + '_' + str(today.minute) + '.csv'

  with open(os.path.dirname(os.path.abspath('weworkremotely_jobs')) + '/weworkremotely_jobs/' + filename, 'w', newline='') as csvfile: # gobi version 
  #with open(os.path.dirname(os.path.abspath('weworkremotely_jobs')) + '/weworkremotely_jobs/' + filename, 'w', encoding='UTF-16', newline='') as csvfile: # anisha version 
    writer = csv.writer(csvfile)
    writer.writerow(['posted_date', 'skills', 'job_name', 'job_type', 'company_name', 'company_location', 'website', 'description', 'ld_link'])

    for link in job_links:
      driver.get(link)
      detail = driver.find_element_by_class_name('content')
      result = detail.get_attribute('innerHTML')
      soup   = BeautifulSoup(result, 'html.parser')

      # Initialization
      job_type  = []
      skills    = []
      company_location = website = 'Not Mentioned'
      
      # Extracting the required data
      job_name      = soup.find("h1").text.strip()
      header        = soup.find("div", class_ = 'listing-header-container').text
      posted_date   = soup.find("div", class_ = 'listing-header-container').find("time").attrs.get('datetime')
      posted_date   = parse(posted_date).date()
      basics        = soup.find("div", class_ = 'listing-header-container').find_all("a")
      description   = soup.find("div", class_ = 'listing-container').text
      company_card  = soup.find("div", class_ = 'company-card')

      # Extracting company's info
      company_name = company_card.find("h2").text
      company_info = company_card.find_all("h3")
      for data in company_info:
        if data.find("a"):
          website = data.find("a").attrs.get('href')
        else:
          company_location = data.text.strip()

      # Arrahge job type details in comma separated values
      for date in basics:
        job_type.append(date.text)
      job_type = ', '.join(job_type)

      # To extract skills from description
      all_text = description + header
      desc = modify(all_text)
      for skill in ld_skills:
        modified = modify(skill).lower()
        if modified in desc.lower():
          skills.append(skill)

      ld_link = get_link(skills, driver)
      writer.writerow([posted_date, skills, job_name, job_type, company_name, company_location, website, description, ld_link])
      print('New job record added: ', job_name)

    print('\nSuccessfully created a new csv file for indeed.com jobs - ' + filename + '.')  
